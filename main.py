import streamlit as st
import asyncio
import ollama

# Template for terrain generation prompt
terrain_generation_template = """
Create a Blender Python script for a terrain based on the following criteria:  
**Terrain Type:** {terrain_type}  
**Polygon Shape:** {polygon_shape}  
**Number of Polygons:** {number_of_polygons}  
**Overall Terrain Size:** {overall_terrain_size}  
**Terrain Details:** {terrain_details}  
**Associated Textures:** {associated_textures}  
**Natural Effects:** {natural_effects}  
**Optimization Settings:** {optimization_settings}  
**Prompt:** {user_prompt}  

**No Extra Content:** Do not include any additional text, comments, or explanations in your response.  
**Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text.  

**If any criterion is None, ignore it completely and do not include it in your response.**  
"""

# Template for getting settings recommendations
recommendation_template = """
Based on the following prompt, give recommendations for the terrain settings (terrain type, polygon shape, etc.) to achieve the best results:  

**Prompt:** {user_prompt}  

**Criteria and Options:**  
- **Terrain Type:** [Plains, Mountains, Desert, Forest, Island, Oceanic, Canyon, Volcanic, Tundra, Savannah]  
- **Polygon Shape:** [Triangles, Squares, Hexagons, Custom]  
- **Number of Polygons:** [1 to 10000]  
- **Terrain Size:** [Small, Medium, Large, Massive]  
- **Terrain Details:** [Jagged Peaks, Smooth Plains, Rugged Cliffs, Deep Valleys, Craters, Plateaus, Rolling Hills, Ravines, Caves]  
- **Associated Textures:** [Grass, Sand, Rock, Snow, Water, Lava, Mud, Dirt, Gravel, Ice]  
- **Natural Effects:** [Erosion, Wind Patterns, River Carving, Volcanic Flow, Glacial Movement, Cracking, Sediment Layers]  
- **Optimization Settings:** [None, Optimized for Mobile, Low-spec Device Friendly, High Performance]  

**Recommendations:**  
- For the following criteria, you can choose **only one option**:  
    - **Terrain Type**  
    - **Polygon Shape**  
    - **Terrain Size**  
    - **Optimization Settings**

- For the following criteria, you can **choose multiple options**:  
    - **Terrain Details**  
    - **Associated Textures**  
    - **Natural Effects**

Please provide your recommendations for each criterion, ensuring the choices follow the options available. If a criterion has multiple options, feel free to suggest more than one. If the criterion has a dropdown, select exactly one option.

**No Extra Content:** Do not include any additional text, comments, or explanations in your response.  
**Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text.  
"""

# Function to generate terrain code
async def generate_terrain_code(prompt, terrain_type, polygon_shape, number_of_polygons, overall_terrain_size, terrain_details, 
                                associated_textures, natural_effects, optimization_settings):
    full_prompt = terrain_generation_template.format(
        terrain_type=terrain_type,
        polygon_shape=polygon_shape,
        number_of_polygons=number_of_polygons,
        overall_terrain_size=overall_terrain_size,
        terrain_details=terrain_details,
        associated_textures=associated_textures,
        natural_effects=natural_effects,
        optimization_settings=optimization_settings,
        user_prompt=prompt
    )

    try:
        response = ollama.chat(model="llama-3.1", messages=[{"role": "user", "content": full_prompt}])
        return response['text']
    except Exception as e:
        st.error(f"Error generating terrain code: {e}")
        return None

# Function to get recommendations from Ollama
async def get_recommendations(user_prompt):
    full_prompt = recommendation_template.format(user_prompt=user_prompt)

    try:
        response = ollama.chat(model="llama-3.1", messages=[{"role": "user", "content": full_prompt}])
        return response['text']
    except Exception as e:
        st.error(f"Error fetching recommendations: {e}")
        return None

# Function to modify terrain code
async def modify_terrain_code(existing_code, modification_prompt):
    full_prompt = modification_template.format(
        shader_code=existing_code,
        modification_prompt=modification_prompt
    )

    try:
        response = ollama.chat(model="llama-3.1", messages=[{"role": "user", "content": full_prompt}])
        return response['text']
    except Exception as e:
        st.error(f"Error modifying terrain code: {e}")
        return None

# Frontend of the Streamlit app
st.title("AI Terrain Generator for Blender")

# Sidebar with app link and usage explanation
with st.sidebar:
    st.header("AI Terrain Generator")
    st.write("This app generates terrain scripts for Blender based on your inputs. Use the options below to customize the terrain and get a Python script for Blender.")
    st.write("[Click here to access the app](#)")

# Terrain Type selection with default to None
terrain_type = st.selectbox("Select Terrain Type", [None, "Plains", "Mountains", "Desert", "Forest", "Island", "Oceanic", "Canyon", "Volcanic", "Tundra", "Savannah"], index=0)

# Polygon Shape and Number selection with default to None
polygon_shape = st.selectbox("Polygon Shape", [None, "Triangles", "Squares", "Hexagons", "Custom"], index=0)
number_of_polygons = st.number_input("Number of Polygons", min_value=1, value=None)

# Overall Terrain Size with default to None
overall_terrain_size = st.selectbox("Terrain Size", [None, "Small", "Medium", "Large", "Massive"], index=0)

# Terrain Details with default to None
terrain_details = st.multiselect("Terrain Details", ["Jagged Peaks", "Smooth Plains", "Rugged Cliffs", "Deep Valleys", "Craters", "Plateaus", "Rolling Hills", "Ravines", "Caves"], default=[])

# Associated Textures with default to None
associated_textures = st.multiselect("Associated Textures", ["Grass", "Sand", "Rock", "Snow", "Water", "Lava", "Mud", "Dirt", "Gravel", "Ice"], default=[])

# Natural Effects with default to None
natural_effects = st.multiselect("Natural Effects", ["Erosion", "Wind Patterns", "River Carving", "Volcanic Flow", "Glacial Movement", "Cracking", "Sediment Layers"], default=[])

# Optimization Settings with default to None
optimization_settings = st.selectbox("Optimization Settings", [None, "None", "Optimized for Mobile", "Low-spec Device Friendly", "High Performance"], index=0)

# Function to handle user inputs and process terrain generation
def handle_terrain_generation():
    user_prompt = st.text_area("Enter your prompt for the terrain generation", "")

    if st.button("Generate Terrain Script"):
        if not user_prompt:
            st.error("Please enter a prompt to generate the terrain script.")
            return
        
        terrain_code = asyncio.run(generate_terrain_code(
            user_prompt=user_prompt,
            terrain_type=terrain_type,
            polygon_shape=polygon_shape,
            number_of_polygons=number_of_polygons,
            overall_terrain_size=overall_terrain_size,
            terrain_details=terrain_details,
            associated_textures=associated_textures,
            natural_effects=natural_effects,
            optimization_settings=optimization_settings
        ))

        if terrain_code:
            st.text_area("Generated Terrain Code", terrain_code, height=400)

# Function to handle user inputs and process terrain recommendations
def handle_recommendations():
    user_prompt = st.text_area("Enter your prompt for terrain recommendations", "")

    if st.button("Get Terrain Recommendations"):
        if not user_prompt:
            st.error("Please enter a prompt to get terrain recommendations.")
            return
        
        recommendations = asyncio.run(get_recommendations(user_prompt))
        
        if recommendations:
            st.text_area("Terrain Recommendations", recommendations, height=400)

# Layout for terrain generation and recommendations
tab_1, tab_2 = st.tabs(["Generate Terrain Script", "Get Terrain Recommendations"])

with tab_1:
    handle_terrain_generation()

with tab_2:
    handle_recommendations()

      
