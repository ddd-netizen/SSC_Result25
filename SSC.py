import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

import os
# Load data

df = pd.read_csv("SSC Result2 24-25.csv")

# Rename columns if necessary (example: remove spaces)
df.columns = [col.strip().replace(" ", "_") for col in df.columns]

# Sidebar filters
st.sidebar.title("🔍 Filter Data")
regions = st.sidebar.multiselect("Select Region(s)", options=df['Region'].unique(), default=df['Region'].unique())
centers = st.sidebar.multiselect("Select Center(s)", options=df['Center'].unique(), default=df['Center'].unique())
genders = st.sidebar.multiselect("Select Gender", options=df['Gender'].unique(), default=df['Gender'].unique())

# Apply filters
filtered_df = df[
    (df['Region'].isin(regions)) &
    (df['Center'].isin(centers)) &
    (df['Gender'].isin(genders))
]

st.title("📊 SSC Dashboard 2024-25")

# KPI metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Students", len(filtered_df))
col2.metric("Average Percentage", round(filtered_df['Percentage'].mean(), 2))

male_count = len(filtered_df[filtered_df['Gender'].str.lower() == 'male'])
female_count = len(filtered_df[filtered_df['Gender'].str.lower() == 'female'])

# Handle division by zero
if female_count > 0:
    gender_ratio = male_count / female_count
    col3.metric(label="Gender Ratio (M:F)", value=f"{gender_ratio:.2f} : 1")
else:
    col3.metric(label="Gender Ratio:** Cannot calculate (No female data)")

#col3.metric("Gender Ratio (F:M)", f"{(filtered_df['Gender'].value_counts().get('F', 0))}:{(filtered_df['Gender'].value_counts().get('M', 0))}")


cl1,cl2,cl3=st.columns(3)
total_students = len(filtered_df)
passed_students = filtered_df['Result'].str.lower().eq('pass').sum()  # case-insensitive match
pass_percentage = (passed_students / total_students) * 100

# Display in Streamlit
cl1.metric(label="Total Students", value=total_students)
cl2.metric(label="Passed Students", value=passed_students)
cl3.metric(label="Pass Percentage", value=f"{pass_percentage:.2f}%")

male_count = len(filtered_df[filtered_df['Gender'].str.lower() == 'male'])
female_count = len(filtered_df[filtered_df['Gender'].str.lower() == 'female'])

# Handle division by zero
if female_count > 0:
    gender_ratio = male_count / female_count
    st.write(f"**Gender Ratio (M:F):** {male_count}:{female_count} or {gender_ratio:.2f} : 1")
else:
    st.write("**Gender Ratio:** Cannot calculate (No female data)")

# Bar Chart: Region-wise student count
st.subheader("👥 Students Count by Region")
region_count = filtered_df['Region'].value_counts().reset_index()
region_count.columns = ['Region', 'Count']
fig_region = px.bar(region_count, x='Region', y='Count', color='Region', title="Region-wise Student Count")
st.plotly_chart(fig_region, use_container_width=True)

# Top 5 Students Overall
st.subheader("🏆 Top 5 Students Overall")
top5 = filtered_df.sort_values(by="Total", ascending=False).head(5)
st.dataframe(top5[['Name', 'Region', 'Center', 'Gender', 'Total', 'Percentage']])

# Top 5 per Region
st.subheader("📈 Pie Chart: Top 5 Students by Region")

# Top 5 students overall from filtered data
top5_students = filtered_df.sort_values(by='Total', ascending=False).head(5)


# Pie Chart: Top 5 Students Region-wise
st.subheader("📈 Pie Chart: Top 5 Students by Region")

# Top 5 students overall from filtered data
top5_students = filtered_df.sort_values(by='Total', ascending=False).head(5)

# Count of students by region among top 5
top5_region_count = top5_students['Region'].value_counts().reset_index()
top5_region_count.columns = ['Region', 'Count']

# Create pie chart
fig_pie = px.pie(
    top5_region_count,
    values='Count',
    names='Region',
    title='Region-wise Distribution of Top 5 Students',
    hole=0.4
)
fig_pie.update_traces(textposition='inside', textinfo='percent+label')

# Show chart
st.plotly_chart(fig_pie, use_container_width=True)


st.subheader("📈 Pie Chart: Top 5 Students by Center")

# Count of students by Center among top 5
top5_center_count = top5_students['Center'].value_counts().reset_index()
top5_center_count.columns = ['Center', 'Count']

# Create pie chart
fig_center_pie = px.pie(
    top5_center_count,
    values='Count',
    names='Center',
    title='Center-wise Distribution of Top 5 Students',
    hole=0.4
)
fig_center_pie.update_traces(textposition='inside', textinfo='percent+label')


gender_counts = filtered_df['Gender'].value_counts()

# Pie chart
fig, ax = plt.subplots()
ax.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=30)
ax.axis('equal')
st.pyplot(fig)
# Show chart
st.plotly_chart(fig_center_pie, use_container_width=True)



# Show full filtered data
with st.expander("📄 Show Full Filtered Data"):
    st.dataframe(filtered_df)
