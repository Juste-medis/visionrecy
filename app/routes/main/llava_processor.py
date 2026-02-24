import torch
import io
import logging
from PIL import Image
from transformers import LlavaProcessor, LlavaForConditionalGeneration, Blip2Processor, Blip2ForConditionalGeneration


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLaVAAnalyzer:
    def __init__(self):
        self.model = None
        self.processor = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_loaded = False

    def load_model(self):
        """Charge le modèle LLaVA"""
        try:
            logger.info("Chargement du modèle LLaVA...")

            # Modèle LLaVA 1.5 - 7B (vous pouvez changer pour une version plus petite)
            model_id = "Vision-CAIR/minigpt4"

            self.processor = Blip2Processor.from_pretrained(
                "Salesforce/blip2-opt-2.7b")
            self.model = Blip2ForConditionalGeneration.from_pretrained(
                "Salesforce/blip2-opt-2.7b", device_map="cpu")

            # self.processor = LlavaProcessor.from_pretrained(model_id)
            # # self.processor.num_additional_tokens = 1
            # self.processor.num_additional_image_tokens = 1

            # self.model = LlavaForConditionalGeneration.from_pretrained(
            #     model_id,
            #     torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            #     low_cpu_mem_usage=True,
            #     device_map="auto"
            # )

            self.model_loaded = True
            logger.info(f"Modèle LLaVA chargé sur {self.device}")

        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle: {str(e)}")
            raise

    def analyze_image(self, image_data, prompt, max_tokens=200, temperature=0.7):
        """
        Analyse une image avec le prompt donné

        Args:
            image_data: bytes ou file-like object de l'image
            prompt: texte du prompt pour l'analyse
            max_tokens: nombre maximum de tokens à générer
            temperature: température pour la génération

        Returns:
            str: résultat de l'analyse
        """
        if not self.model_loaded:
            self.load_model()

        try:
            # Charger l'image depuis les données bytes
            image = Image.open(io.BytesIO(image_data)).convert('RGB')

            # Préparer les entrées
            # inputs = self.processor(
            #     text=prompt,
            #     images=image,
            #     return_tensors="pt",
            #     padding=True
            # )
            # Préparer les entrées
            inputs = self.processor(
                image,
                prompt
            )

            # Déplacer les entrées sur le device approprié
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            # Générer la réponse
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    do_sample=True,
                    temperature=temperature,
                    top_p=0.9,
                    pad_token_id=self.processor.tokenizer.eos_token_id
                )

            # Décoder la réponse
            response = self.processor.decode(
                outputs[0],
                skip_special_tokens=True
            )

            # Nettoyer la réponse (enlever le prompt)
            if prompt in response:
                response = response.replace(prompt, "").strip()

            return response

        except Exception as e:
            logger.error(f"Erreur lors de l'analyse: {str(e)}")
            raise


# Instance globale
llava_analyzer = LLaVAAnalyzer()
