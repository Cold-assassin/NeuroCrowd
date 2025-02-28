import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation.model import CrowdModel
from simulation.panic_detector import PanicAnalyzer
from config.settings import Config

# Initialize components
model = CrowdModel()
analyzer = PanicAnalyzer()

# ========== Helper Functions ==========
def get_gate_populations(model):
    """Calculate population with simulated redistribution"""
    # Original population calculation
    gates = {
        "Gate 1": {"x": (0, 10), "y": (0, 10)},
        "Gate 2": {"x": (40, 49), "y": (0, 10)},
        "Gate 3": {"x": (20, 30), "y": (45, 49)},
        "Gate 4": {"x": (0, 10), "y": (40, 49)},
        "Gate 5": {"x": (40, 49), "y": (40, 49)},
        "Gate 6": {"x": (40, 30), "y": (35, 49)},
        "Gate 7": {"x": (45, 40), "y": (40, 49)},
    }
    
    populations = {}
    for gate, area in gates.items():
        count = 0
        for x in range(max(0, area["x"][0]), min(Config.GRID_WIDTH, area["x"][1]+1)):
            for y in range(max(0, area["y"][0]), min(Config.GRID_HEIGHT, area["y"][1]+1)):
                count += len(model.grid.get_cell_list_contents((x, y)))
        populations[gate] = count
    
    # Add chaos simulation overlay
    if hasattr(st.session_state, 'chaos_triggered'):
        transfer_rate = 4  # Increased transfer rate for emergency
        populations["Gate 1"] = max(0, populations["Gate 1"] - transfer_rate)
        populations["Gate 5"] = min(100, populations["Gate 5"] + transfer_rate)
        
    return populations

def create_gate_chart(gate_data):
    """Create animated bar chart with dynamic updates"""
    # Check chaos condition
    if not hasattr(st.session_state, 'chaos_triggered') and gate_data["Gate 1"] > 70:
        st.session_state.chaos_triggered = True
        st.session_state.chaos_start_time = time.time()
    
    # If chaos detected, modify the data
    if hasattr(st.session_state, 'chaos_triggered'):
        chaos_duration = time.time() - st.session_state.chaos_start_time
        if chaos_duration < 15:  # Show effect for 15 seconds
            gate_data["Gate 1"] = max(30, gate_data["Gate 1"] - 3)
            gate_data["Gate 5"] = min(100, gate_data["Gate 5"] + 3)

    # Create figure with dynamic colors
    colors = ['#00ff9d'] * 5
    if hasattr(st.session_state, 'chaos_triggered'):
        colors[0] = '#ff0000'  # Red for Gate 1
        colors[4] = '#00ff00'  # Green for Gate 5

    fig = go.Figure(data=[
        go.Bar(
            x=list(gate_data.keys()),
            y=list(gate_data.values()),
            marker=dict(
                color=colors,
                line=dict(color='#00ff9d', width=1)
            )
        )
    ])
    
    # Add chaos warning annotation
    if hasattr(st.session_state, 'chaos_triggered'):
        fig.add_annotation(
            x=0.5,
            y=1.2,
            xref="paper",
            yref="paper",
            text="🚨 CHAOS DETECTED! Redirecting crowd to Gate 5 🚨",
            showarrow=False,
            font=dict(size=14, color='#ff0000'),
            bgcolor="rgba(0,0,0,0.5)"
        )
    
    # Keep the rest of the layout configuration same
    fig.update_layout(
        height=250,
        margin=dict(t=30, b=20, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00ff9d', size=12),
        xaxis=dict(showgrid=True, gridcolor='#00ff9d', gridwidth=0.5),
        yaxis=dict(showgrid=True, gridcolor='#00ff9d', gridwidth=0.5)
    )
    return fig


def create_density_map(grid_data):
    """Create properly sized density map"""
    fig = px.imshow(
        grid_data,
        color_continuous_scale='hot',
        height=500,  # Reduced height for better spacing
        width=800     # Fixed width for consistency
    )
    fig.update_layout(
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig
# ========== UI Configuration ==========
st.set_page_config(layout="wide", page_icon="🌐")

st.markdown("""
<style>
    .stApp {
        background: #0a0a2e;
        color: #00ff9d;
    }
    .stMarkdown {
        margin-bottom: 1rem !important;
    }
    .block-container {
        padding: 2rem 1rem;
    }
    .stButton>button {
        width: 100%;
        border: 2px solid #00ff9d !important;
    }
    .stProgress .st-bo {
        background-color: #00ff9d !important;
    }
</style>
""", unsafe_allow_html=True)

# ========== Main Application ==========
def main():
    st.title("🌐 Crowd Control Dashboard")
    
    # Initialize chaos timer
    if 'chaos_start' not in st.session_state:
        st.session_state.chaos_start = time.time() + 11  # Set chaos start time
    
    # Main layout columns
    left_col, right_col = st.columns([1, 2], gap="large")

    with left_col:
        # System Status Panel
        with st.container():
            st.subheader("🚪 Gate Status")
            gate_data = get_gate_populations(model)
            st.plotly_chart(create_gate_chart(gate_data), use_container_width=True)

        # Control Panel
        with st.container():
            st.subheader("🎛️ Controls")
            st.button("🔄 Emergency Reset")
            st.selectbox("Simulation Speed", ["1x", "2x", "5x"], key="speed")
            st.toggle("AI Override Mode", value=True, key="ai_toggle")

    with right_col:
        # Main Visualization
        with st.container():
            st.subheader("🌋 Live Density Map")
            grid = np.zeros((Config.GRID_WIDTH, Config.GRID_HEIGHT))
            for cell in model.grid.coord_iter():
                grid[cell[1]] = len(cell[0])
            st.plotly_chart(create_density_map(grid), use_container_width=True)

        # Threat Analysis
        with st.container():
            st.subheader("🚨 Threat Detection")
            input_text = st.text_area("Social Media Monitor:", 
                                    "Crowd getting too dense at Gate 1!")
            panic_level = analyzer.analyze(input_text)
            st.progress(panic_level/100, f"Panic Level: {panic_level}/100")

    # Bottom Status Bar
    st.markdown("""
    <div style='
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #001a1a;
        padding: 10px;
        border-top: 2px solid #00ff9d33;
        display: flex;
        justify-content: space-between;
        z-index: 999;
    '>
        <span>🟢 System Status: Operational</span>
        <span>Last Update: {time}</span>
        <span>Agents: {agents}</span>
    </div>
    """.format(
        time=time.strftime("%H:%M:%S"),
        agents=Config.INITIAL_AGENTS
    ), unsafe_allow_html=True)

    # Simulation loop
    while True:
         if time.time() > st.session_state.chaos_start and not hasattr(st.session_state, 'chaos_triggered'):
            st.session_state.chaos_triggered = True
            st.experimental_rerun()
        
            model.step()
            time.sleep(0.2)

if __name__ == "__main__":
    main()

gate 6 and 7 bar is not coming and like after redirecting it showed turn again green instead of red and use your creativty also you want