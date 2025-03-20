import streamlit as st
import datetime
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import pandas as pd
import numpy as np

# Page config
st.set_page_config(
    page_title="Four Generations of War - Siren Visualization",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: black;
        color: white;
    }
    h1, h2, h3 {
        color: red !important;
    }
    .stButton button {
        background-color: gray;
        color: white;
    }
    .bottom-message {
        color: red;
        font-weight: bold;
        font-size: 24px;
        text-align: center;
        margin-top: 30px;
    }
    .family-card {
        background-color: #111;
        border-radius: 10px;
        padding: 10px;
        margin: 10px;
    }
    /* Dark theme overrides */
    .css-1kyxreq {
        background-color: black;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for storing family members
if 'family_members' not in st.session_state:
    st.session_state.family_members = []
    
# Title
st.markdown("<h1 style='text-align: center; color: red;'>My First Siren</h1>", unsafe_allow_html=True)

# Sidebar for adding family members
with st.sidebar:
    st.header("Add Family Member")
    
    relation = st.text_input("Relation (Father, Mother, Son, etc.)")
    name = st.text_input("Name")
    birth_year = st.number_input("Year of Birth", min_value=1900, 
                               max_value=datetime.datetime.now().year, 
                               value=1980, step=1)
    siren_year = st.number_input("Year of First Siren", min_value=1900, 
                               max_value=datetime.datetime.now().year, 
                               value=2000, step=1)
    
    if st.button("Add Family Member"):
        if not name:
            st.error("Name is required")
        elif siren_year < birth_year:
            st.error("First Siren year cannot be before birth year")
        else:
            st.session_state.family_members.append({
                "relation": relation,
                "name": name,
                "birth_year": int(birth_year),
                "siren_year": int(siren_year)
            })
            st.success(f"Added {name}")

# Display current family members
if st.session_state.family_members:
    st.subheader("Family Members")
    
    # Create columns for the grid layout
    cols = st.columns(3)
    
    for i, member in enumerate(st.session_state.family_members):
        with cols[i % 3]:
            with st.container():
                st.markdown(f"<div class='family-card'>", unsafe_allow_html=True)
                
                # Calculate age
                current_year = datetime.datetime.now().year
                age = current_year - member["birth_year"]
                
                # Display member info
                st.markdown(f"**{member['name']}**")
                st.markdown(f"{member['relation']}")
                st.markdown(f"Born: {member['birth_year']}")
                st.markdown(f"First Siren: {member['siren_year']}")
                
                # Remove button
                if st.button(f"Remove", key=f"remove_{i}"):
                    st.session_state.family_members.pop(i)
                    st.experimental_rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Add family members using the sidebar")

# Function to generate the visualization image
def generate_visualization():
    if not st.session_state.family_members:
        st.error("Please add at least one family member")
        return None
        
    # Create image
    width, height = 800, 1000
    image = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(image)
    
    # Try to use fonts - streamlit runs on various platforms, so we use a fallback approach
    try:
        title_font = ImageFont.truetype("arial.ttf", 40)
        name_font = ImageFont.truetype("arial.ttf", 24)
        info_font = ImageFont.truetype("arial.ttf", 18)
        message_font = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        # Default system font as fallback
        title_font = ImageFont.load_default()
        name_font = ImageFont.load_default()
        info_font = ImageFont.load_default()
        message_font = ImageFont.load_default()
    
    # Draw title
    title_text = "My First Siren"
    try:
        title_width = draw.textlength(title_text, font=title_font)
    except (AttributeError, TypeError):
        # For older versions of PIL
        title_width = draw.textsize(title_text, font=title_font)[0]
    
    draw.text(((width - title_width) // 2, 40), title_text, font=title_font, fill="red")
    
    # Calculate layout
    num_members = len(st.session_state.family_members)
    cols = min(3, num_members)
    rows = (num_members + cols - 1) // cols
    
    cell_width = width // cols
    cell_height = 180
    start_y = 120
    
    current_year = datetime.datetime.now().year
    
    # Draw family members
    for i, member in enumerate(st.session_state.family_members):
        row, col = i // cols, i % cols
        x_center = col * cell_width + cell_width // 2
        y_top = start_y + row * cell_height
        
        # Calculate age and icon size
        age = current_year - member["birth_year"]
        icon_size = max(30, min(80, 30 + age//2))
        
        # Draw person icon (head)
        head_radius = icon_size // 4
        draw.ellipse([(x_center - head_radius, y_top), 
                     (x_center + head_radius, y_top + head_radius*2)], 
                     fill="white")
        
        # Body
        draw.line([(x_center, y_top + head_radius*2), 
                  (x_center, y_top + icon_size - head_radius)], 
                  fill="white", width=2)
        
        # Arms
        draw.line([(x_center - icon_size//4, y_top + icon_size//2), 
                  (x_center + icon_size//4, y_top + icon_size//2)], 
                  fill="white", width=2)
        
        # Legs
        draw.line([(x_center, y_top + icon_size - head_radius),
                  (x_center - icon_size//6, y_top + icon_size)],
                  fill="white", width=2)
        
        draw.line([(x_center, y_top + icon_size - head_radius),
                  (x_center + icon_size//6, y_top + icon_size)],
                  fill="white", width=2)
        
        # Text information
        name_text = member["name"]
        try:
            name_width = draw.textlength(name_text, font=name_font)
        except (AttributeError, TypeError):
            # For older versions of PIL
            name_width = draw.textsize(name_text, font=name_font)[0]
            
        draw.text((x_center - name_width//2, y_top + icon_size + 10), 
                 name_text, font=name_font, fill="white")
        
        born_text = f"Born: {member['birth_year']}"
        try:
            born_width = draw.textlength(born_text, font=info_font)
        except (AttributeError, TypeError):
            # For older versions of PIL
            born_width = draw.textsize(born_text, font=info_font)[0]
            
        draw.text((x_center - born_width//2, y_top + icon_size + 40), 
                 born_text, font=info_font, fill="white")
        
        siren_text = f"First Siren: {member['siren_year']}"
        try:
            siren_width = draw.textlength(siren_text, font=info_font)
        except (AttributeError, TypeError):
            # For older versions of PIL
            siren_width = draw.textsize(siren_text, font=info_font)[0]
            
        draw.text((x_center - siren_width//2, y_top + icon_size + 65), 
                 siren_text, font=info_font, fill="white")
    
    # Messages at the bottom
    message_y = start_y + rows * cell_height + 50
    
    message1 = "End This Fuc*ing War!"
    try:
        message1_width = draw.textlength(message1, font=message_font)
    except (AttributeError, TypeError):
        # For older versions of PIL
        message1_width = draw.textsize(message1, font=message_font)[0]
        
    draw.text(((width - message1_width) // 2, message_y), 
             message1, font=message_font, fill="red")
    
    message2 = "Bring them Home Now!"
    try:
        message2_width = draw.textlength(message2, font=message_font)
    except (AttributeError, TypeError):
        # For older versions of PIL
        message2_width = draw.textsize(message2, font=message_font)[0]
        
    draw.text(((width - message2_width) // 2, message_y + 50), 
             message2, font=message_font, fill="red")
    
    return image

# Button to generate visualization
if st.button("Generate Visualization"):
    with st.spinner("Generating visualization..."):
        image = generate_visualization()
        
        if image:
            # Display the image
            st.image(image, caption="Four Generations of War - Siren Visualization")
            
            # Create a download link
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            # Link for download
            href = f"data:image/png;base64,{base64.b64encode(byte_im).decode()}"
            st.markdown(f'<a href="{href}" download="siren_visualization.png"><button style="background-color: gray; color: white; padding: 10px; border-radius: 5px;">Download Image</button></a>', unsafe_allow_html=True)

# Display bottom messages
st.markdown("<div class='bottom-message'>End This Fuc*ing War!</div>", unsafe_allow_html=True)
st.markdown("<div class='bottom-message'>Bring them Home Now!</div>", unsafe_allow_html=True)

# Instructions for sharing
st.sidebar.markdown("## Sharing")
st.sidebar.markdown("""
To share this visualization:
1. Generate the visualization
2. Download the image
3. Share on social media with hashtags:
   - #FourGenerationsOfWar
   - #BringThemHomeNow
""")
