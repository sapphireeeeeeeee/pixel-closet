import streamlit as st
from PIL import Image
import base64
import json
import os
from google import genai
from google.genai import types

# Page layout setup
st.set_page_config(page_title="~\(≧▽≦)/~", layout="centered")

# Initialize api_key variable
api_key = None

# Read strictly from your key.toml file
if os.path.exists("key.toml"):
    try:
        with open("key.toml", "r") as f:
            for line in f:
                if "GEMINI_API_KEY" in line:
                    api_key = line.split("=")[1].strip().strip('"').strip("'")
    except Exception:
        pass

# Fallback: show the sidebar input box only if key.toml is missing or broken
if not api_key:
    st.sidebar.title("🎀 Setup")
    api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

# Helper function to convert your JPG image into a format CSS can read
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Function to load your local TrueType font file safely
def load_custom_font(font_path):
    if os.path.exists(font_path):
        with open(font_path, "rb") as f:
            font_data = base64.b64encode(f.read()).decode()
        return f"""
        @font-face {{
            font-family: 'Soria';
            src: url(data:font/ttf;base64,{font_data}) format('truetype');
        }}
        """
    return ""

try:
    bg_base64 = get_base64_image("holographic.jpg")
    font_css = load_custom_font("Soria font.ttf") 
    
    st.markdown(
        f"""
        <style>
        {font_css}

        .stApp {{
            background-image: url("data:image/jpeg;base64,{bg_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        
        /* 📜 Apply custom font to text elements but strictly protect built-in icons */
        .stApp p:not([data-testid="stIconMaterial"]), 
        .stApp label:not([data-testid="stIconMaterial"]),
        .stApp span:not([data-testid="stIconMaterial"]) {{
            color: #1E1E24 !important;
            font-family: 'Soria', serif !important;
            font-size: 1.35rem !important;
        }}
        
        /* 🏷️ Project name title wrapper rule */
        #project-title {{
            font-size: 5.5rem !important;
            color: #1E1E24 !important;
            font-family: 'Soria', serif !important;
            font-weight: bold !important;
            letter-spacing: 1px !important;
            line-height: 1.1 !important;
            display: block !important;
            text-align: center !important;
            margin-bottom: 0px !important;
            padding-bottom: 0px !important;
        }}
        
        /* 🎀 Card Header Settings */
        .stApp h3 {{
            font-size: 1.85rem !important;
            color: #1E1E24 !important;
            font-family: 'Soria', serif !important;
            font-weight: bold !important; 
            letter-spacing: 0.5px;
        }}
        
        .stApp h2, .stApp h4, .stApp h5, .stApp h6 {{
            color: #1E1E24 !important;
            font-family: 'Soria', serif !important;
            font-weight: normal !important; 
            letter-spacing: 0.5px;
        }}
        
        /* 🛡️ CRITICAL FIXED SHIELD FOR STREAMLIT MATERIAL ICONS 🛡️ */
        [data-testid="stIconMaterial"] {{
            font-family: "Material Symbols Rounded" !important;
            font-size: inherit !important;
            font-weight: normal !important;
            font-style: normal !important;
            display: inline-block !important;
        }}
        
        /* 🎀 Dreamy Uploader Container Customization 🎀 */
        .stFileUploader {{
            background-color: rgba(255, 255, 255, 0.4) !important;
            backdrop-filter: blur(5px);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.02);
            border: 2px dashed rgba(255, 255, 255, 0.6) !important;
        }}
        
        [data-testid="stFileUploaderDropzone"] {{
            background-color: rgba(255, 255, 255, 0.5) !important;
            border: none !important;
            padding: 20px !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            gap: 10px !important;
        }}
        
        /* Ensure the dropzone button lays out elements side-by-side cleanly */
        [data-testid="stFileUploaderDropzone"] button {{
            background-color: rgba(255, 255, 255, 0.7) !important;
            border: 1px solid rgba(0, 0, 0, 0.1) !important;
            border-radius: 8px !important;
            transition: all 0.3s ease;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 8px !important;
            width: auto !important;
            padding: 6px 16px !important;
        }}
        
        [data-testid="stFileUploaderDropzone"] button:hover {{
            background-color: rgba(255, 255, 255, 0.9) !important;
            border-color: rgba(0, 0, 0, 0.2) !important;
            box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.05);
        }}
        
        /* Adjust font style inside the button text specifically */
        [data-testid="stFileUploaderDropzone"] button p {{
            font-size: 1.1rem !important;
            font-family: 'Soria', serif !important;
            margin: 0 !important;
        }}
        
        /* Clear styling for file specifications text underneath the button */
        [data-testid="stFileUploaderDropzone"] div [data-testid="stMarkdownContainer"] p {{
            font-size: 1.05rem !important;
            font-family: 'Soria', serif !important;
            color: #1E1E24 !important;
        }}
        
        [data-testid="stFileUploaderFileName"] {{
            background-color: rgba(255, 255, 255, 0.8) !important;
            color: #1E1E24 !important;
            border-radius: 8px;
        }}

        /* 🎀 White Transparent Cards with Dotted Borders 🎀 */
        .closet-card {{
            background-color: rgba(255, 255, 255, 0.45) !important;
            backdrop-filter: blur(8px);
            padding: 20px;
            border-radius: 14px;
            margin-bottom: 15px;
            box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.03);
            border: 2px dotted rgba(255, 255, 255, 0.8) !important;
        }}
        
        .closet-card h3 {{
            margin-top: 0px !important;
            padding-top: 0px !important;
        }}

        /* ✨ Fixed Font Sizing: Decreased and stripped of italics for clean presentation ✨ */
        code, .closet-card i, .closet-card em {{
            background-color: transparent !important;
            color: #4A4E69 !important;
            padding: 0px !important;
            font-family: 'Soria', serif !important;
            font-size: 1.15rem !important; 
            font-style: normal !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
except FileNotFoundError:
    st.warning("⚠️ Make sure 'holographic.jpg' is saved inside the exact same folder!")

# Main layout titles
st.markdown("<div id='project-title'>✨ pixel closet ✨</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.45rem !important; margin-top: 10px !important;'>drop an item inside and watch your dream outfit arrange itself~</p>", unsafe_allow_html=True)
st.write("---")

uploaded = st.file_uploader("drop an item inside 💌", type=["jpg", "jpeg", "png"])

if uploaded:
    image = Image.open(uploaded).convert("RGB")
    
    top_col1, top_col2 = st.columns([1, 1], gap="large")
    
    with top_col1:
        st.image(image, caption="your uploaded piece", use_container_width=True)

    if not api_key:
        st.warning("Please make sure your Gemini API Key is saved inside key.toml as GEMINI_API_KEY = 'your_key'")
    else:
        with st.spinner("assembling the look... ☁️"):
            try:
                client = genai.Client(api_key=api_key)
                
                styling_prompt = """
                You are a premium, highly specific fashion AI stylist specializing in coquette, subculture, 
                Y2K, j-fashion, aesthetic, and casual streetwear. Analyze this clothing image.
                
                Provide a JSON response matching exactly this structure:
                {
                  "piece": "Short descriptive name of item type (e.g., Frilly Halter Top, Ruffled Asymmetric Maxi Skirt)",
                  "palette": "Primary color name + undertone description",
                  "has_layout": true, 
                  "layout_label": "What to pair it with (e.g., Low-rise utility cargos, Pleated denim mini skirt). Set to null ONLY if the item is a full-body dress.",
                  "footwear": "Specific footwear recommendation customized precisely to this exact item's vibe",
                  "bag": "Specific bag/handbag recommendation customized to this style",
                  "jewelry": "Jewelry accents that tie this specific style together",
                  "match_note": "A sweet, one-sentence styling tip telling them how to blend this specific item into an outfit layout using complementary colors."
                }
                Do not include any markdown formatting or markdown blocks like ```json in your response. Return raw text only.
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[image, styling_prompt]
                )
                
                ai_data = json.loads(response.text.strip())
                
                with top_col2:
                    st.markdown(f"""
                    <div class="closet-card">
                        <h3>📝 closet notes</h3>
                        <p>the piece: <code>{ai_data['piece']}</code></p>
                        <p>the palette: <code>{ai_data['palette']}</code></p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.write("---")
                
                if ai_data.get('has_layout') and ai_data.get('layout_label'):
                    st.markdown(f"""
                    <div class="closet-card">
                        <h3>✨ outfit layout</h3>
                        <p>🌼 match with:<br><em>{ai_data['layout_label']}</em></p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.write("---")
                    
                st.markdown(f"""
                <div class="closet-card">
                    <h3>🎀 complete the look 🎀</h3>
                    <p>🦋 footwear pairing:<br><em>{ai_data['footwear']}</em></p>
                    <p>👝 handbag pairing:<br><em>{ai_data['bag']}</em></p>
                    <p>✨ jewelry accents:<br><em>{ai_data['jewelry']}</em></p>
                </div>
                """, unsafe_allow_html=True)
                st.write("---")
                
                st.success(f"🍓 *match note: {ai_data['match_note']}*")
                    
            except Exception as e:
                st.error(f"Styling engine encountered an error: {e}")


#python -m streamlit run app.py