import streamlit as st
from datetime import date
import pandas as pd
from database import (
    add_task,
    get_tasks,
    update_task,
    delete_task,
    update_completed
)

st.set_page_config(
    page_title="Smart Task Manager",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>

/* Main page */
.main {
    background-color: #f8f9fa;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: black;
    padding: 15px;
    border-radius: 15px;
    border: 2px solid #e6e6e6;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
}

[data-testid="stMetricLabel"] {
    color: black !important;
    font-weight: bold;
}

[data-testid="stMetricValue"] {
    color: black !important;
    font-size: 40px;
    font-weight: bold;
}
            
div[data-testid="stMetric"] {
    background: pink;
    border-radius: 15px;
    padding: 20px;
    border: 2px solid #d9d9d9;
}


/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 10px;
    font-weight: bold;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: black;
}

</style>
""", unsafe_allow_html=True)
priority_filter = st.selectbox(
    "Priority Filter",
    [
        "All",
        "🔴 High",
        "🟡 Medium",
        "🟢 Low"
    ]
)
category_filter = st.selectbox(
    "Category Filter",
    [
        "All",
        "📚 Study",
        "💼 Work",
        "🛒 Shopping",
        "🏠 Personal"
    ]
)
status_filter = st.selectbox(
    "Status Filter",
    [
        "All",
        "Completed",
        "Pending"
    ]
)

from database import (
    add_task,
    get_tasks,
    update_task,
    delete_task,
    update_completed
)

st.title("🚀 Smart Task Manager")

st.caption("Organize • Prioritize • Achieve 🚀")

st.sidebar.title("🚀 Smart Task Manager")

st.sidebar.header("📋 Add New Task")

if "tasks" not in st.session_state:

    db_tasks = get_tasks()

    st.session_state.tasks = []

    for task in db_tasks:

        st.session_state.tasks.append({
            "task": task[1],
            "priority": task[2],
            "category": task[3],
            "due_date": task[4],
            "completed": bool(task[5])
        })

if "editing_task" not in st.session_state:
    st.session_state.editing_task = None

task = st.sidebar.text_input("Enter a new task")

priority = st.sidebar.selectbox(
    "Select Priority",
    ["🔴 High", "🟡 Medium", "🟢 Low"]
)

category = st.sidebar.selectbox(
    "Select Category",
    ["📚 Study", "💼 Work", "🛒 Shopping", "🏠 Personal"]
)

due_date = st.sidebar.date_input("Select Due Date")
st.sidebar.divider()
st.sidebar.info(
    "💡 Tip: Complete your high-priority tasks first!"
)

if st.sidebar.button("➕ Add Task"):
    if task.strip() != "":
        st.session_state.tasks.append({
    "task": task,
    "priority": priority,
    "category": category,
    "due_date": due_date,
    "completed": False
})
        
        add_task(
            task,
            priority,
            category,
            str(due_date),
            0
        )  

        st.rerun() 


st.divider()
st.subheader("📋 My Tasks")

search = st.text_input("🔍 Search Tasks")

st.divider()
st.markdown("## 🎯 Filter Tasks")
sort_option = st.selectbox(
    "Sort Tasks By",
    [
        "Default",
        "Priority",
        "Due Date",
        "Category",
        "Task Name"
    ]
)

tasks_to_show = st.session_state.tasks.copy()
filtered_tasks = []

for task in tasks_to_show:

    if priority_filter != "All":
        if task["priority"] != priority_filter:
            continue

    if category_filter != "All":
        if task["category"] != category_filter:
            continue

    if status_filter == "Completed":
        if not task["completed"]:
            continue

    elif status_filter == "Pending":
        if task["completed"]:
            continue

    filtered_tasks.append(task)

tasks_to_show = filtered_tasks
priority_order = {
    "🔴 High": 1,
    "🟡 Medium": 2,
    "🟢 Low": 3
} 
if sort_option == "Priority":
    tasks_to_show.sort(
        key=lambda task: priority_order[task["priority"]]
    )

elif sort_option == "Due Date":
    tasks_to_show.sort(
        key=lambda task: task["due_date"]
    )

elif sort_option == "Category":
    tasks_to_show.sort(
        key=lambda task: task["category"]
    )

elif sort_option == "Task Name":
    tasks_to_show.sort(
        key=lambda task: task["task"].lower()
    ) 

for i, task in enumerate(tasks_to_show):

    if search.lower() not in task["task"].lower():
        continue

    col1, col2, col3 = st.columns([5,1,1])

    with col1:

        completed = st.checkbox(
            "",
            value=task["completed"],
            key=f"complete_{i}"
        )

        if completed != task["completed"]:

            update_completed(
                task["task"],
                int(completed)
            )

        task["completed"] = completed 

        today = date.today()

        task_date = date.fromisoformat(str(task["due_date"]))

        overdue = (
            task_date < today
            and not task["completed"]
        )
        
        
        if task["completed"]:

            st.success(
                    f"""
            ✅ {task['task']}

            {task['priority']} | {task['category']}

            📅 Due: {task['due_date']}
            """
                )

        else:

            st.info(
                f"""
        📌 {task['task']}

        {task['priority']} | {task['category']}

        📅 Due: {task['due_date']}
        """
           ) 

    with col2:

        if st.button("✏️", key=f"edit_{i}"):
            st.session_state.editing_task = i

        if st.session_state.editing_task == i:

            new_task = st.text_input(
                "Edit Task",
                value=task["task"],
                key=f"edit_text_{i}"
            )

            if st.button("Save", key=f"save_{i}"):

                old_task = st.session_state.tasks[i]["task"]

                update_task(old_task, new_task)

                st.session_state.tasks[i]["task"] = new_task

                st.session_state.editing_task = None

                st.rerun()

    with col3:

        if st.button("❌", key=f"delete_{i}"):

            task_name = st.session_state.tasks[i]["task"]

            delete_task(task_name)

            st.session_state.tasks.pop(i)

            st.rerun()
        

total_tasks = len(st.session_state.tasks)

completed_tasks = sum(
    task["completed"] for task in st.session_state.tasks
)

pending_tasks = total_tasks - completed_tasks

today = date.today()

overdue_count = 0
today_count = 0

for task in st.session_state.tasks:

    due = date.fromisoformat(str(task["due_date"]))

    if not task["completed"]:

        if due < today:
            overdue_count += 1

        elif due == today:
            today_count += 1

study_tasks = sum(
    task["category"] == "📚 Study"
    for task in st.session_state.tasks
)

work_tasks = sum(
    task["category"] == "💼 Work"
    for task in st.session_state.tasks
)

shopping_tasks = sum(
    task["category"] == "🛒 Shopping"
    for task in st.session_state.tasks
)

personal_tasks = sum(
    task["category"] == "🏠 Personal"
    for task in st.session_state.tasks
)

today = date.today()

upcoming_tasks = []
today_tasks = []

for task in st.session_state.tasks: 
    
    due = date.fromisoformat(str(task["due_date"]))

    if due == today and not task["completed"]:
        today_tasks.append(task)

    days_left = (due - today).days

    if (
        not task["completed"]
        and 0 <= days_left <= 7
    ):
        upcoming_tasks.append(task)

overdue_tasks = sum(
    1
    for task in st.session_state.tasks
    if (
        date.fromisoformat(str(task["due_date"])) < today
        and not task["completed"]
    )
)
st.markdown("---")

if overdue_count > 0:
    st.error(f"⚠️ You have {overdue_count} overdue task(s)!")

elif today_count > 0:
    st.warning(f"📅 You have {today_count} task(s) due today!")

else:
    st.success("🎉 Great! No overdue tasks.") 
st.subheader("📅 Today's Tasks")

if len(today_tasks) == 0:

    st.success("🎉 No tasks due today!")

else:

    for task in today_tasks:

        st.warning(
            f"""
📌 {task['task']}

{task['priority']}

📂 {task['category']}
"""
        )
st.subheader("🔔 Upcoming Tasks")
if len(upcoming_tasks) == 0:

    st.success("🎉 No upcoming tasks.")

else:

    for task in upcoming_tasks:

        st.info(
            f"""
📌 {task['task']}

📅 Due: {task['due_date']}

{task['priority']}
"""
        )

col1, col2 = st.columns(2)

with col1:
    st.metric("📋 Total Tasks", total_tasks)

with col2:
    st.metric("✅ Completed", completed_tasks)

col3, col4 = st.columns(2)

with col3:
    st.metric("⏳ Pending", pending_tasks)

with col4:
    st.metric("🔴 Overdue", overdue_tasks)

df = pd.DataFrame(st.session_state.tasks)

csv = df.to_csv(index=False)

excel_file = "tasks.xlsx"

df.to_excel(
    excel_file,
    index=False
)

st.download_button(
    label="📥 Download Tasks as CSV",
    data=csv,
    file_name="tasks.csv",
    mime="text/csv"
)

st.download_button(
    label="📥 Download Tasks as Excel",
    data=open(excel_file, "rb").read(),
    file_name=excel_file,
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

if total_tasks > 0:
    progress = completed_tasks / total_tasks

    st.subheader("📊 Progress")

    st.progress(progress)

    percentage = round(progress * 100)

    st.write(
        f"✅ {completed_tasks}/{total_tasks} Tasks Completed ({percentage}%)"
    )

    st.markdown("---")
    st.caption(
    "🚀 Smart Task Manager | Made using Streamlit & SQLite"
)