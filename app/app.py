import streamlit as st
from backend import Prediction

extract = Prediction()

# Page config
st.set_page_config(page_title="CO₂ Emission Predictor", page_icon="🌍", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f9f9f9;
    }
    h1 {
        color: #2c3e50;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .prediction-box {
        background-color: #ffffff;
        border: 2px solid #27ae60;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background-color: #27ae60;
        color: white;
        border-radius: 8px;
        padding: 0.6em 1.2em;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🌍 CO₂ Emission Prediction Dashboard")
st.markdown("### Predict vehicle CO₂ emissions based on engine and fuel characteristics.")

# Sidebar for inputs
st.sidebar.header("🔧 Input Parameters")

make_options = list(extract.extract_make())
make_options.insert(0, '-- Select an option --')
make = st.sidebar.selectbox("Company Name", options=make_options)

if make != make_options[0]:
    model_options = list(extract.extract_model(make=make))
    model_options.insert(0, '-- Select an option --')
    model = st.sidebar.selectbox("Model Type", options=model_options)

    if model != model_options[0]:
        transmission_options = list(extract.extract_transmission(model=model))
        transmission_options.insert(0, '-- Select an option --')
        transmission = st.sidebar.selectbox("Transmission Type", options=transmission_options)

        if transmission != transmission_options[0]:
            fuel_options = list(extract.extract_fuel(model=model, transmission=transmission))
            fuel_options.insert(0, '-- Select an option --')
            fuel = st.sidebar.selectbox("Fuel Type", options=fuel_options)

            if fuel != fuel_options[0]:
                engine, cylinder = extract.extract_engine_cylinder(make=make, transmission=transmission)
                engine = list(engine)
                cylinder = list(cylinder)
                cylinder.sort()

                engine_size = st.sidebar.slider("Engine Size (L)", min_value=1.0, max_value=max(engine), value=1.0, step=0.5)
                cylinders_no = st.sidebar.radio("No. of cylinders", options=cylinder)
                fuel_consumption = st.sidebar.number_input("Fuel Consumption (L/100km)",
                                                                placeholder="Enter fuel consumption of your car..",format="%.1f")
                
                        

# Main layout with two columns
col1, col2 = st.columns([2, 1])

with col1:
    st.image("images/car.jpg",
             caption="Vehicle emissions illustration", width=700)

with col2:
    if st.button("🔮 Predict Emissions"):
        predicted_result = extract.predict(engine_size, cylinders_no, fuel_consumption, make, transmission, fuel, model)

        st.markdown(f"""
            <div class="prediction-box">
                <h2 style="color:#e74c3c">Estimated CO₂ Emissions:</h2>
                <h1 style="color:#2980b9">{predicted_result} g/km</h1>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Build for accurate prediction | Interactive Dashboard 🚗")
