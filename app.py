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

# Add custom CSS for styling - enhanced poster look
st.markdown("""
<style>
    .main {
        background-color: black;
        color: white;
    }
    h1 {
        color: red !important;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        text-shadow: 2px 2px 4px #000000;
    }
    h2, h3 {
        color: red !important;
        font-weight: bold;
    }
    .stButton button {
        background-color: #555;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        border: 1px solid #777;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
    }
    .stButton button:hover {
        background-color: #700;
        border-color: red;
    }
    .bottom-message {
        color: red;
        font-weight: 800;
        font-size: 2.2rem;
        text-align: center;
        margin-top: 30px;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-shadow: 1px 1px 3px #000000;
    }
    .family-card {
        background-color: #111;
        border-radius: 10px;
        padding: 15px;
        margin: 10px;
        border: 1px solid #333;
        box-shadow: 0 4px 8px rgba(0,0,0,0.5);
    }
    /* Dark theme overrides */
    .css-1kyxreq {
        background-color: black;
    }
    .stSidebar {
        background-color: #111;
    }
    .gender-select .stRadio > div {
        flex-direction: row;
    }
    .gender-select .stRadio label {
        margin-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for storing family members
if 'family_members' not in st.session_state:
    st.session_state.family_members = []
    
# Title with larger text
st.markdown("<h1 style='text-align: center; color: red;'>My First Siren</h1>", unsafe_allow_html=True)

# Sidebar for adding family members
with st.sidebar:
    st.header("Add Family Member")
    
    relation = st.text_input("Relation (Father, Mother, Son, etc.)")
    name = st.text_input("Name")
    
    # Gender selection with radio buttons
    st.markdown('<div class="gender-select">', unsafe_allow_html=True)
    gender = st.radio("Gender", options=["Male", "Female"], horizontal=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
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
                "gender": gender,
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
                st.markdown(f"<h3 style='margin-bottom: 5px;'>{member['name']}</h3>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size: 18px;'>{member['relation']} ({member['gender']})</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size: 16px;'>Born: {member['birth_year']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size: 16px;'>First Siren: {member['siren_year']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size: 16px;'>Age at First Siren: {member['siren_year'] - member['birth_year']}</div>", unsafe_allow_html=True)
                
                # Remove button
                if st.button(f"Remove", key=f"remove_{i}"):
                    st.session_state.family_members.pop(i)
                    st.experimental_rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Add family members using the sidebar")

# Function to draw a better male icon
def draw_male_icon(draw, x_center, y_top, icon_size, color="white"):
    head_radius = icon_size // 4
    
    # Head - circle
    draw.ellipse([(x_center - head_radius, y_top), 
                 (x_center + head_radius, y_top + head_radius*2)], 
                 fill=color)
    
    # Body - slightly wider
    body_length = icon_size - head_radius*2 - 10
    draw.line([(x_center, y_top + head_radius*2), 
              (x_center, y_top + head_radius*2 + body_length)], 
              fill=color, width=3)
    
    # Arms - angled slightly
    shoulder_y = y_top + head_radius*2 + body_length//4
    arm_length = icon_size//3
    
    # Left arm
    draw.line([(x_center, shoulder_y), 
              (x_center - arm_length, shoulder_y + arm_length//2)], 
              fill=color, width=3)
    
    # Right arm
    draw.line([(x_center, shoulder_y), 
              (x_center + arm_length, shoulder_y + arm_length//2)], 
              fill=color, width=3)
    
    # Legs - angled
    hip_y = y_top + head_radius*2 + body_length
    leg_length = icon_size//3
    
    # Left leg
    draw.line([(x_center, hip_y),
              (x_center - leg_length//2, hip_y + leg_length)],
              fill=color, width=3)
    
    # Right leg
    draw.line([(x_center, hip_y),
              (x_center + leg_length//2, hip_y + leg_length)],
              fill=color, width=3)

# Function to draw a better female icon
def draw_female_icon(draw, x_center, y_top, icon_size, color="white"):
    head_radius = icon_size // 4
    
    # Head - circle
    draw.ellipse([(x_center - head_radius, y_top), 
                 (x_center + head_radius, y_top + head_radius*2)], 
                 fill=color)
    
    # Body - triangle dress shape
    body_length = icon_size - head_radius*2 - 10
    top_width = icon_size//8
    bottom_width = icon_size//2
    
    # Triangle dress
    draw.polygon([
        (x_center, y_top + head_radius*2),  # top
        (x_center - bottom_width, y_top + head_radius*2 + body_length),  # bottom left
        (x_center + bottom_width, y_top + head_radius*2 + body_length)   # bottom right
    ], outline=color, width=2)
    
    # Arms
    shoulder_y = y_top + head_radius*2 + body_length//5
    arm_length = icon_size//3
    
    # Slightly curved arms
    # Left arm
    draw.line([(x_center, shoulder_y), 
              (x_center - arm_length, shoulder_y)], 
              fill=color, width=2)
    
    # Right arm
    draw.line([(x_center, shoulder_y), 
              (x_center + arm_length, shoulder_y)], 
              fill=color, width=2)
    
    # Legs
    leg_y = y_top + head_radius*2 + body_length
    leg_length = icon_size//4
    
    # Left leg
    draw.line([(x_center - leg_length//3, leg_y),
              (x_center - leg_length//3, leg_y + leg_length)],
              fill=color, width=2)
    
    # Right leg
    draw.line([(x_center + leg_length//3, leg_y),
              (x_center + leg_length//3, leg_y + leg_length)],
              fill=color, width=2)

# Function to generate the visualization image with enhanced poster style
def generate_visualization():
    if not st.session_state.family_members:
        st.error("Please add at least one family member")
        return None
        
    # Create image - larger for poster style
    width, height = 1200, 1600
    image = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(image)
    
    # Try to use fonts - enhanced larger sizes for poster
    try:
        title_font = ImageFont.truetype("arial.ttf", 80)
        name_font = ImageFont.truetype("arial.ttf", 40)
        info_font = ImageFont.truetype("arial.ttf", 30)
        message_font = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        try:
            # Try loading default fonts with larger sizes
            title_font = ImageFont.load_default().font_variant(size=80)
            name_font = ImageFont.load_default().font_variant(size=40)
            info_font = ImageFont.load_default().font_variant(size=30)
            message_font = ImageFont.load_default().font_variant(size=60)
        except:
            # Fallback to default
            title_font = ImageFont.load_default()
            name_font = ImageFont.load_default()
            info_font = ImageFont.load_default()
            message_font = ImageFont.load_default()
    
    # Draw title - larger, more prominent
    title_text = "MY FIRST SIREN"
    try:
        title_width = draw.textlength(title_text, font=title_font)
    except (AttributeError, TypeError):
        # For older versions of PIL
        title_width = draw.textsize(title_text, font=title_font)[0]
    
    # Draw title with slight shadow effect for poster look
    shadow_offset = 3
    draw.text(((width - title_width) // 2 + shadow_offset, 60 + shadow_offset), 
             title_text, font=title_font, fill="#550000")
    draw.text(((width - title_width) // 2, 60), 
             title_text, font=title_font, fill="#FF0000")
    
    # Add a subtle horizontal line under title
    line_y = 160
    draw.line([(width//4, line_y), (3*width//4, line_y)], fill="#770000", width=3)
    
    # Calculate layout
    num_members = len(st.session_state.family_members)
    cols = min(3, num_members)
    rows = (num_members + cols - 1) // cols
    
    cell_width = width // cols
    cell_height = 320  # Larger cells for poster style
    start_y = 200  # Start lower to accommodate larger title
    
    current_year = datetime.datetime.now().year
    
    # Draw family members
    for i, member in enumerate(st.session_state.family_members):
        row, col = i // cols, i % cols
        x_center = col * cell_width + cell_width // 2
        y_top = start_y + row * cell_height
        
        # Calculate age and icon size - larger icons for poster
        age = current_year - member["birth_year"]
        icon_size = max(60, min(160, 60 + age))
        
        # Draw gender-specific icon
        if member["gender"] == "Male":
            draw_male_icon(draw, x_center, y_top, icon_size)
        else:
            draw_female_icon(draw, x_center, y_top, icon_size)
        
        # Text information - larger and more prominent
        name_text = member["name"]
        try:
            name_width = draw.textlength(name_text, font=name_font)
        except (AttributeError, TypeError):
            # For older versions of PIL
            name_width = draw.textsize(name_text, font=name_font)[0]
            
        # Draw name with slight shadow for poster effect
        name_y = y_top + icon_size + 20
        draw.text((x_center - name_width//2 + 2, name_y + 2), 
                 name_text, font=name_font, fill="#333333")
        draw.text((x_center - name_width//2, name_y), 
                 name_text, font=name_font, fill="white")
        
        # Draw info text
        info_y = name_y + 50
        
        born_text = f"Born: {member['birth_year']}"
        try:
            born_width = draw.textlength(born_text, font=info_font)
        except (AttributeError, TypeError):
            born_width = draw.textsize(born_text, font=info_font)[0]
            
        draw.text((x_center - born_width//2, info_y), 
                 born_text, font=info_font, fill="white")
        
        siren_text = f"First Siren: {member['siren_year']}"
        try:
            siren_width = draw.textlength(siren_text, font=info_font)
        except (AttributeError, TypeError):
            siren_width = draw.textsize(siren_text, font=info_font)[0]
            
        draw.text((x_center - siren_width//2, info_y + 40), 
                 siren_text, font=info_font, fill="white")
        
        # Add age at first siren
        age_at_siren = member['siren_year'] - member['birth_year']
        age_text = f"Age at First Siren: {age_at_siren}"
        try:
            age_width = draw.textlength(age_text, font=info_font)
        except (AttributeError, TypeError):
            age_width = draw.textsize(age_text, font=info_font)[0]
            
        draw.text((x_center - age_width//2, info_y + 80), 
                 age_text, font=info_font, fill="white")
    
    # Messages at the bottom - larger and more impactful for poster
    message_y = start_y + rows * cell_height + 160
    
    # Add a subtle decorative line above messages
    draw.line([(width//5, message_y - 80), (4*width//5, message_y - 80)], 
             fill="#770000", width=4)
    
    message1 = "END THIS FUC*ING WAR!"
    try:
        message1_width = draw.textlength(message1, font=message_font)
    except (AttributeError, TypeError):
        message1_width = draw.textsize(message1, font=message_font)[0]
    
    # Draw message with shadow for poster effect    
    shadow_offset = 3
    draw.text(((width - message1_width) // 2 + shadow_offset, message_y + shadow_offset), 
             message1, font=message_font, fill="#550000")
    draw.text(((width - message1_width) // 2, message_y), 
             message1, font=message_font, fill="#FF0000")
    
    message2 = "BRING THEM HOME NOW!"
    try:
        message2_width = draw.textlength(message2, font=message_font)
    except (AttributeError, TypeError):
        message2_width = draw.textsize(message2, font=message_font)[0]
    
    # Draw second message with shadow    
    draw.text(((width - message2_width) // 2 + shadow_offset, message_y + 80 + shadow_offset), 
             message2, font=message_font, fill="#550000")
    draw.text(((width - message2_width) // 2, message_y + 80), 
             message2, font=message_font, fill="#FF0000")
    
    # Add a subtle decorative line below messages
    draw.line([(width//5, message_y + 160), (4*width//5, message_y + 160)], 
             fill="#770000", width=4)
    
    return image

# Button to generate visualization
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Generate Visualization Poster", use_container_width=True):
        with st.spinner("Generating poster visualization..."):
            image = generate_visualization()
            
            if image:
                # Display the image
                st.image(image, caption="Four Generations of War - Siren Visualization Poster")
                
                # Create a download link
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                # Link for download with better styling
                download_label = "Download Poster"
                href = f"data:image/png;base64,{base64.b64encode(byte_im).decode()}"
                st.markdown(f"""
                <div style="text-align: center; margin-top: 20px;">
                  <a href="{href}" download="siren_visualization_poster.png">
                    <button style="background-color: #700; color: white; padding: 12px 24px; border-radius: 5px; 
                    border: none; font-size: 1.2rem; font-weight: bold; cursor: pointer; transition: all 0.3s;">
                      {download_label}
                    </button>
                  </a>
                </div>
                """, unsafe_allow_html=True)

# Display bottom messages
st.markdown("<div class='bottom-message'>End This Fuc*ing War!</div>", unsafe_allow_html=True)
st.markdown("<div class='bottom-message'>Bring them Home Now!</div>", unsafe_allow_html=True)

# Enhanced instructions for sharing
st.sidebar.markdown("## Sharing")
st.sidebar.markdown("""
### How to Share:
1. Generate the visualization poster
2. Download the high-quality image
3. Share on social media with hashtags:
   - #FourGenerationsOfWar
   - #MyFirstSiren
   - #BringThemHomeNow
""")

# About section
st.sidebar.markdown("## About This Visualization")
st.sidebar.markdown("""
This visualization creates a powerful statement about the generational impact of war. 
By showing when each family member first experienced war sirens, it highlights how 
conflicts span across multiple generations.

The size of each person icon represents their age, creating a visual representation 
of how war affects people throughout their lifetime.
""")
