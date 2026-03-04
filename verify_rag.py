import os
import sys
import logging
import json

# Add current directory to path
sys.path.append(os.getcwd())

from rag_pipeline1 import RAGPipeline1
from rag_pipeline2 import RAGPipeline2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def verify_rag():
    # Try to load GOOGLE_API_KEY from environment or secrets.toml
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        try:
            import toml
            secrets = toml.load(os.path.join(".streamlit", "secrets.toml"))
            google_api_key = secrets.get("GOOGLE_API_KEY")
        except Exception:
            pass

    if not google_api_key:
        print("[ERROR] GOOGLE_API_KEY not found in environment or .streamlit/secrets.toml.")
        return

    PDF_FOLDER = r"C:\Users\A.Kumarasiri\OneDrive - CGIAR\WETLAND CHATBOT DOCUMENT\ALL"
    INDEX_FILE = "pdf_index_enhanced1.pkl"

    models_to_test = ["models/gemma-3-4b-it", "models/gemma-3-12b-it"]
    
    for model_name in models_to_test:
        print("\n" + "#"*60)
        print(f" TESTING MODEL: {model_name} ")
        print("#"*60)
        
        model_params = {
            "google_api_key": google_api_key,
            "model_name": model_name
        }

        try:
            # Select correct pipeline version
            if "12b" in model_name:
                pipeline_class = RAGPipeline2
                print(f"[INFO] Using RAGPipeline2 for {model_name}")
            else:
                pipeline_class = RAGPipeline1
                print(f"[INFO] Using RAGPipeline1 for {model_name}")

            pipeline = pipeline_class(
                pdf_folder=PDF_FOLDER,
                index_file=INDEX_FILE,
                model_params=model_params
            )

            if not pipeline.load_index():
                print(f"[RETRY] Failed to load index for {model_name}.")
                continue

            test_queries = [
                "What is the definition of a 'wetland' according to Sri Lankan policy?",
                "What are the main objectives of the National Wetland Policy of Sri Lanka?",
                "List the specific penalties for unauthorized construction in wetlands according to the SLLRDC Act."
            ]

            for query in test_queries:
                print(f"\n[QUERY] Querying {model_name}: {query}")
                try:
                    answer = pipeline.query(query)
                    print(f"\n[SUCCESS] Result:\n{answer}")
                except Exception as e:
                    print(f"[ERROR] during query with {model_name}: {e}")
            
            print("\n" + "="*50)

        except Exception as e:
            print(f"[ERROR] during pipeline initialization for {model_name}: {e}")

if __name__ == "__main__":
    verify_rag()
