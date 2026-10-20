import os
import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# --- CONFIGURATION & DATA ---
FILE = "students.csv"
COORDS = {
    "Surat": (72.83, 21.17),
    "Ahmedabad": (72.57, 23.02),
    "Vadodara": (73.18, 22.31),
    "Rajkot": (70.80, 22.30),
    "Mumbai": (72.88, 19.08)
}

# Initialize CSV if it doesn't exist
if not os.path.exists(FILE):
    pd.DataFrame({
        "Roll No": [101, 102, 103, 104, 105],
        "Name": ["Aarav", "Diya", "Rohan", "Priya", "Neel"],
        "Course": ["BCA", "BTech", "BCA", "BSc", "BTech"],
        "City": ["Surat", "Ahmedabad", "Vadodara", "Rajkot", "Surat"],
        "Marks": [85, 78, 92, 65, 74],
        "Attendance": [90, 85, 95, 70, 80]
    }).to_csv(FILE, index=False)

# Helper function to load data
def load_data():
    return pd.read_csv(FILE)

# --- WEB APP UI SETUP ---
st.set_page_config(page_title="Student Management System", page_icon="🎓", layout="wide")
st.title("🎓 Student Management System")
st.markdown("A simple, data-driven system to manage and analyze student records.")

# Sidebar Navigation
st.sidebar.header("Navigation")
menu = [
    "View Students", 
    "Add Student", 
    "Search Student", 
    "Delete Student", 
    "Performance Analysis", 
    "Geographical Analysis"
]
choice = st.sidebar.radio("Go to:", menu)

# --- MENU ROUTING ---

if choice == "View Students":
    st.subheader("📋 All Student Records")
    df = load_data()
    # Display as an interactive dataframe
    st.dataframe(df, use_container_width=True)

elif choice == "Add Student":
    st.subheader("➕ Add New Student")
    
    # Create an input form
    with st.form("add_student_form"):
        roll = st.number_input("Roll No", min_value=1, step=1)
        name = st.text_input("Name")
        course = st.text_input("Course")
        city = st.text_input("City (e.g., Surat, Ahmedabad)")
        marks = st.number_input("Marks", min_value=0.0, max_value=100.0)
        attendance = st.number_input("Attendance (%)", min_value=0.0, max_value=100.0)
        
        submitted = st.form_submit_button("Add Student")
        
        if submitted:
            df = load_data()
            if roll in df["Roll No"].values:
                st.error(f"Roll number {roll} already exists!")
            else:
                new_data = pd.DataFrame([{
                    "Roll No": roll, "Name": name, "Course": course,
                    "City": city.title(), "Marks": marks, "Attendance": attendance
                }])
                df = pd.concat([df, new_data], ignore_index=True)
                df.to_csv(FILE, index=False)
                st.success(f"Student {name} added successfully!")

elif choice == "Search Student":
    st.subheader("🔍 Search Student")
    search_roll = st.number_input("Enter Roll Number to search:", min_value=1, step=1)
    
    if st.button("Search"):
        df = load_data()
        result = df[df["Roll No"] == search_roll]
        if not result.empty:
            st.success("Student Found!")
            st.dataframe(result, use_container_width=True)
        else:
            st.warning("Student not found.")

elif choice == "Delete Student":
    st.subheader("🗑️ Delete Student")
    del_roll = st.number_input("Enter Roll Number to delete:", min_value=1, step=1)
    
    if st.button("Delete"):
        df = load_data()
        if del_roll in df["Roll No"].values:
            df = df[df["Roll No"] != del_roll]
            df.to_csv(FILE, index=False)
            st.success(f"Record for Roll No {del_roll} deleted.")
        else:
            st.warning("Student not found.")

elif choice == "Performance Analysis":
    st.subheader("📊 Performance & City Analysis")
    df = load_data()
    
    # Display top-level metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Average Marks", f"{round(df['Marks'].mean(), 2)}")
    col2.metric("Average Attendance", f"{round(df['Attendance'].mean(), 2)}%")
    col3.metric("Pass (Marks >= 40)", (df["Marks"] >= 40).sum())
    col4.metric("Fail (Marks < 40)", (df["Marks"] < 40).sum())
    
    # Show two plots side by side
    st.markdown("---")
    fig_col1, fig_col2 = st.columns(2)
    
    with fig_col1:
        st.markdown("**Student Marks**")
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        df.plot(x="Name", y="Marks", kind="bar", ax=ax1, color="teal", legend=False)
        ax1.set_ylim(0, 100)
        ax1.set_ylabel("Marks")
        st.pyplot(fig1)
        
    with fig_col2:
        st.markdown("**Students by City**")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        df["City"].value_counts().plot(kind="bar", ax=ax2, color="coral")
        ax2.set_ylabel("Number of Students")
        st.pyplot(fig2)

elif choice == "Geographical Analysis":
    st.subheader("🗺️ Student Geographical Distribution")
    df = load_data()
    
    # Map cities to coordinates
    df["Longitude"] = df["City"].map(lambda c: COORDS.get(c, (None, None))[0])
    df["Latitude"] = df["City"].map(lambda c: COORDS.get(c, (None, None))[1])
    df = df.dropna(subset=["Longitude", "Latitude"])
    
    if df.empty:
        st.warning("No recognized city coordinates found in the dataset.")
    else:
        # Aggregate data
        cities = df.groupby("City").agg(
            Longitude=("Longitude", "first"),
            Latitude=("Latitude", "first"),
            Students=("Roll No", "count")
        ).reset_index()

        # Create GeoPandas dataframe
        gdf = gpd.GeoDataFrame(
            cities,
            geometry=gpd.points_from_xy(cities.Longitude, cities.Latitude),
            crs="EPSG:4326"
        )

        # Plot the map
        fig, ax = plt.subplots(figsize=(10, 6), dpi=120)
        fig.patch.set_facecolor("#F3F6FB")
        ax.set_facecolor("white")
        ax.grid(linestyle="--", alpha=0.25)

        gdf.plot(ax=ax, color="#14B8A6", markersize=180, edgecolor="white", linewidth=2)

        for _, row in gdf.iterrows():
            ax.annotate(
                f"{row.City}\n{row.Students} student(s)",
                (row.geometry.x, row.geometry.y),
                xytext=(0, 15), textcoords="offset points",
                ha="center", fontsize=9, fontweight="bold"
            )

        ax.set_title("Student Mapping by Region", fontsize=14, fontweight="bold", pad=20)
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.spines[["top", "right"]].set_visible(False)
        
        # Display the matplotlib plot in Streamlit
        st.pyplot(fig)