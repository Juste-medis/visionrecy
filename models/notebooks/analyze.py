# from transformers import LlavaNextProcessor, LlavaNextForConditionalGeneration
# import torch
# from PIL import Image
# import requests
# import time

# # Désactiver CUDA et forcer l'utilisation du CPU
# torch.cuda.is_available = lambda: False


# def analyze_image_with_llava(image_path, question="What is shown in this image?"):
#     """
#     Analyse une image avec LLaVA sur CPU
#     """
#     print("🔄 Chargement du modèle LLaVA...")
#     start_time = time.time()

#     try:
#         # Charger le processeur et le modèle (version CPU)
#         processor = LlavaNextProcessor.from_pretrained(
#             "llava-hf/llava-v1.6-mistral-7b-hf"
#         )

#         model = LlavaNextForConditionalGeneration.from_pretrained(
#             "llava-hf/llava-v1.6-mistral-7b-hf",
#             torch_dtype=torch.float32,  # Utiliser float32 au lieu de float16 pour CPU
#             low_cpu_mem_usage=True,
#             device_map="cpu"  # Forcer l'utilisation du CPU
#         )

#         load_time = time.time() - start_time
#         print(f"✅ Modèle chargé en {load_time:.2f} secondes")

#         # Charger l'image
#         print("📸 Chargement de l'image...")
#         if image_path.startswith('http'):
#             image = Image.open(requests.get(image_path, stream=True).raw)
#         else:
#             image = Image.open(image_path)

#         # Préparer la conversation
#         conversation = [
#             {
#                 "role": "user",
#                 "content": [
#                     {"type": "text", "text": question},
#                     {"type": "image"},
#                 ],
#             },
#         ]

#         # Formater le prompt
#         prompt = processor.apply_chat_template(
#             conversation, add_generation_prompt=True
#         )

#         # Préparer les inputs
#         inputs = processor(
#             images=image,
#             text=prompt,
#             return_tensors="pt"
#         )

#         # Génération avec le modèle
#         print("🔍 Analyse de l'image en cours...")
#         generation_start = time.time()

#         output = model.generate(
#             **inputs,
#             max_new_tokens=150,  # Réduire un peu pour CPU
#             do_sample=True,
#             temperature=0.2,
#             top_p=0.95,
#             pad_token_id=processor.tokenizer.eos_token_id
#         )

#         generation_time = time.time() - generation_start
#         print(f"✅ Analyse terminée en {generation_time:.2f} secondes")

#         # Décoder la réponse
#         response = processor.decode(output[0], skip_special_tokens=True)

#         # Nettoyer la réponse (enlever le prompt)
#         if "ASSISTANT:" in response:
#             response = response.split("ASSISTANT:")[-1].strip()

#         total_time = time.time() - start_time
#         print(f"⏱️ Temps total: {total_time:.2f} secondes")

#         return response

#     except Exception as e:
#         print(f"❌ Erreur: {e}")
#         return None

# # Version optimisée avec gestion de mémoire


# def analyze_image_optimized(image_path, question="What is shown in this image?"):
#     """
#     Version optimisée pour CPU avec gestion de mémoire
#     """
#     print("🔄 Chargement du modèle LLaVA (version optimisée)...")

#     try:
#         # Charger seulement ce dont on a besoin
#         from transformers import AutoProcessor, AutoModelForVision2Seq

#         processor = AutoProcessor.from_pretrained(
#             "llava-hf/llava-v1.6-mistral-7b-hf"
#         )

#         model = AutoModelForVision2Seq.from_pretrained(
#             "llava-hf/llava-v1.6-mistral-7b-hf",
#             torch_dtype=torch.float32,
#             device_map="cpu",
#             low_cpu_mem_usage=True
#         )

#         # Charger et prétraiter l'image
#         if image_path.startswith('http'):
#             image = Image.open(requests.get(image_path, stream=True).raw)
#         else:
#             image = Image.open(image_path)

#         # Préparer les inputs
#         inputs = processor(
#             text=question,
#             images=image,
#             return_tensors="pt"
#         )

#         # Génération
#         print("🔍 Analyse en cours...")
#         with torch.no_grad():
#             output = model.generate(
#                 **inputs,
#                 max_new_tokens=100,
#                 do_sample=True,
#                 temperature=0.1  # Température plus basse pour plus de cohérence
#             )

#         # Décoder
#         response = processor.decode(output[0], skip_special_tokens=True)
#         return response

#     except Exception as e:
#         print(f"❌ Erreur: {e}")
#         return None
#  # Version avec gestion de mémoire explicite


# def analyze_image_with_memory_management(image_path):
#     """
#     Version avec gestion manuelle de la mémoire pour éviter les fuites
#     """
#     import gc

#     try:
#         # Nettoyer la mémoire avant de commencer
#         gc.collect()
#         torch.cuda.empty_cache() if torch.cuda.is_available() else None

#         processor = LlavaNextProcessor.from_pretrained(
#             "llava-hf/llava-v1.6-mistral-7b-hf"
#         )

#         model = LlavaNextForConditionalGeneration.from_pretrained(
#             "llava-hf/llava-v1.6-mistral-7b-hf",
#             torch_dtype=torch.float32,
#             device_map="cpu"
#         )

#         # Charger l'image
#         image = Image.open(image_path) if not image_path.startswith('http') else \
#             Image.open(requests.get(image_path, stream=True).raw)

#         # Préparer la conversation
#         conversation = [
#             {
#                 "role": "user",
#                 "content": [
#                     {"type": "text", "text": "Décris cette image en détail en français."},
#                     {"type": "image"},
#                 ],
#             },
#         ]

#         prompt = processor.apply_chat_template(
#             conversation, add_generation_prompt=True)
#         inputs = processor(images=image, text=prompt, return_tensors="pt")

#         # Génération
#         output = model.generate(**inputs, max_new_tokens=200)
#         response = processor.decode(output[0], skip_special_tokens=True)

#         # Nettoyer
#         del processor, model, inputs, output
#         gc.collect()

#         return response

#     except Exception as e:
#         print(f"Erreur: {e}")
#         return None


# # Exemple d'utilisation
# if __name__ == "__main__":
#     # Test avec une image locale
#     image_path = "https://jataietatdeslieu.adidome.com/api/uploads/IMG_6544.jpg"

#     print("🤖 Démarrage de l'analyse LLaVA sur CPU...")
#     result = analyze_image_with_llava(
#         image_path,
#         """Analyse cette image d'une pièce et fournis une réponse structurée en JSON en français.
#     Pour chaque élément visible, indique:
#     - élément: le type d'élément (mur, sol, plafond, fenêtre, porte, meuble, équipement)
#     - couleur: la couleur principale
#     - état: excellent, bon, moyen, mauvais, très mauvais
#     - matériau: si identifiable
#     - remarques: observations supplémentaires

#     Réponds UNIQUEMENT avec du JSON valide sans texte supplémentaire. Format:
#     {
#         "analyse_globale": "description générale",
#         "elements": [
#             {
#                 "element": "type",
#                 "couleur": "couleur",
#                 "etat": "état",
#                 "materiau": "matériau",
#                 "remarques": "observations"
#             }
#         ],
#         "resume": {
#             "nombre_elements": 0,
#             "etat_moyen": "moyen"
#         }
#     }"""
#     )

#     if result:
#         print("\n📋 RÉSULTAT DE L'ANALYSE:")
#         print("=" * 50)
#         print(result)
#         print("=" * 50)
#     else:
#         print("❌ L'analyse a échoué")


import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base")

img_url = 'https://jataietatdeslieu.adidome.com/api/uploads/IMG_6544.jpg'
raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')

# conditional image captioning.
text = "a photography of"
inputs = processor(raw_image, text, return_tensors="pt")

out = model.generate(**inputs)
print(processor.decode(out[0], skip_special_tokens=True))
# >>> a photography of a woman and her dog

# unconditional image captioning
inputs = processor(raw_image, return_tensors="pt")

out = model.generate(**inputs)
print(processor.decode(out[0], skip_special_tokens=True))
