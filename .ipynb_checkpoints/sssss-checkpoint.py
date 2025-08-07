from random import randint
import tkinter as tk
from tkinter import ttk
from tkinter import *

import random
time_slots = ["8:00-10:00", "10:00-12:00", "12:00-2:00", "2:00-4:00", "4:00-6:00"]
days = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday']

# professors = [
#     ['Dr. samir', [('chemistry', 4), ('biology', 2), ('math', 2), ('history', 2)]],
#     ['Dr. 7uda', [('math', 4), ('physics', 2), ('biology', 2), ('chemistry', 2)]],
#     ['Dr. tifa', [('biology', 4), ('history', 2), ('chemistry', 2), ('math', 2)]],
#     ['Dr. nono', [('history', 4), ('math', 2), ('chemistry', 2), ('physics', 2)]]
# ]
professors = []
def select_rand(prof, t, days):
    schedule = []
    for p in prof:
        prof_name = p[0]
        for course in p[1]:
            course_name = course[0]
            course_hours = course[1]
            time = course_hours // 2
            for i in range(time):
                rand_days = random.choice(days)
                rand_t = random.choice(t)
                schedule.append([prof_name, course_name, course_hours, rand_t, rand_days])

    return schedule


def population(c, prof, t, d):
    return [select_rand(prof, t, d) for _ in range(c)]


def many_pop(c, l, prof, t, d):
    return [population(l, prof, t, d) for _ in range(c)]
def fit_2d(pop):
    c = 0
    for i, d in enumerate(pop):
        for x in pop[i + 1:]:
            if x[3] == d[3] and x[4] == d[4]:
                c += 1
    return c


def fitness(pop):
    return [fit_2d(x) for x in pop]


def evolve(pop, retain=0.2, random_select=0.05, mutate=0.01):
    fit = fitness(pop)
    graded = list(zip(pop, fit))
    graded = sorted(graded, key=lambda x: x[1])
    sorted_pop = [x[0] for x in graded]
    retain_length = int(len(sorted_pop) * retain)
    parents = sorted_pop[:retain_length]

    for i in sorted_pop[retain_length:]:
        if random.random() < random_select:
            parents.append(i)

    for i in parents:
        if mutate > random.random():
            pos_to_mutate = randint(0, len(i) - 1)
            i[pos_to_mutate][3] = random.choice(time_slots)
            i[pos_to_mutate][4] = random.choice(days)

            # pos_to_mutate2=randint(0,len(i)-1)
            # col=randint(3,4)
            # i[pos_to_mutate1][col],i[pos_to_mutate2][col]=i[pos_to_mutate2][col],i[pos_to_mutate1][col]
    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []
    while len(children) < desired_length:
        male = randint(0, parents_length - 1)
        female = randint(0, parents_length - 1)
        child = []
        if male != female:
            male = parents[male]
            female = parents[female]
            for k in range(len(male)):

                entry = male[k][:3] + female[k][3:]
                child.append(entry)
            children.append(child)

    parents.extend(children)
    return parents

def add_course():
    course_name = course_entry.get().strip().lower()
    try:
        hours = int(hours_entry.get())
        #
        if hours % 2 != 0:
            hours += 1
    except ValueError:
        return
    if course_name and hours > 0:
        course_listbox.insert(END, f"{course_name},{hours}")
        course_entry.delete(0, END)
        hours_entry.delete(0, END)


def save_professor():
    name = name_entry.get().strip()
    if not name:
        return

    courses = []
    for i in range(course_listbox.size()):
        item = course_listbox.get(i)
        cname, chours = item.split(",")
        courses.append((cname, int(chours)))

    if courses:
        professors.append([name, courses])
        name_entry.delete(0, END)
        course_listbox.delete(0, END)


def finish_entry():
    save_professor()
    entry_window.destroy()  # Close input window and proceed

    # Generate and display schedule
    x = population(200, professors, time_slots, days)
    y = evolve(x)
    z = []
    for i in range(300):
        y = evolve(y)
        for x in y:
            if fit_2d(x) == 0:
                z = x
                break
        if z:
            break

    if z:

        show_table(z)



entry_window = Tk()
entry_window.title("Add Professors and Courses")
entry_window.geometry("400x400")

Label(entry_window, text="Professor Name:").pack()
name_entry = Entry(entry_window)
name_entry.pack()

Label(entry_window, text="Course Name:").pack()
course_entry = Entry(entry_window)
course_entry.pack()

Label(entry_window, text="Hours:").pack()
hours_entry = Entry(entry_window)
hours_entry.pack()

Button(entry_window, text="Add Course", command=add_course).pack()
course_listbox = Listbox(entry_window)
course_listbox.pack(fill=BOTH, expand=True)

Button(entry_window, text="Save Professor", command=save_professor).pack()
Button(entry_window, text="Finish", command=finish_entry).pack()

entry_window.mainloop()

# Define available time slots




# def fitness(population):
#     fitness_values = []
#
#     for schedule in population:
#         conflict_count = 0
#         hours_tracker = {}
#
#         for i, row1 in enumerate(schedule):
#             prof1, course1, hours1, day1, time1 = row1
#
#             # Track hours
#             key = (prof1, course1)
#             # Assume each scheduled session is 2 hours (from your times like 8:00-10:00)
#             hours_tracker[key] = hours_tracker.get(key, 0) + 1
#
#             # Conflict checking
#             for j, row2 in enumerate(schedule):
#                 if i < j:
#                     prof2, course2, hours2, day2, time2 = row2
#
#                     if day1 == day2 and time1 == time2:
#                         conflict_count += 1
#
#         # After scanning all rows, check if assigned hours > required hours
#         overflow_penalty = 0
#         for (prof, course), assigned_hours in hours_tracker.items():
#             # Find the original required hours for this course
#             for row in schedule:
#                 if row[0] == prof and row[1] == course:
#                     required_hours = row[2]
#                     break
#
#             if assigned_hours > required_hours:
#                 overflow_penalty += assigned_hours - required_hours  # Penalize for extra hours
#
#         total_penalty = conflict_count + overflow_penalty
#         fitness_values.append(total_penalty)
#
#     return fitness_values





def grade(pop, target):
    sum = 0
    for x in professors:
        sum += len(x[1])
    f = fitness(pop)

    res = abs(((f[target] / sum) * 100) - 100)
    return res


x = population(700, professors, time_slots, days)
y = evolve(x)
z = []
for i in range(800):
    y = evolve(y)
    for x in y:
        if fit_2d(x) == 0:
            z = x
            break;
    if z:  # If we found a valid schedule, break the loop
        break

print("Found schedule:", z)  # Debug print


def show_table(schedule):
    # Create a new root window
    root = Tk()
    root.title("Timetable Matrix")
    root.geometry("1200x600")  # Increased window size

    # Define days and time slots in consistent order
    sorted_days = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday']
    sorted_slots = ["8:00-10:00", "10:00-12:00", "12:00-2:00", "2:00-4:00", "4:00-6:00"]

    # Build matrix: day -> time -> content
    matrix = {day: {slot: "" for slot in sorted_slots} for day in sorted_days}
    for prof, course, hours, time, day in schedule:
        cell = f"{prof}\n({course})"
        if matrix[day][time]:
            matrix[day][time] += "\n" + cell  # Handle multiple entries in same slot
        else:
            matrix[day][time] = cell

    # Create Treeview with increased cell height
    cols = ['Day'] + sorted_slots
    tree = ttk.Treeview(root, columns=cols, show='headings', height=10)  # Increased height
    for col in cols:
        tree.heading(col, text=col)
        if col == 'Day':
            tree.column(col, width=150, anchor='center')  # Wider day column
        else:
            tree.column(col, width=200, anchor='center')  # Wider time slot columns

    # Configure row height
    style = ttk.Style()
    style.configure('Treeview', rowheight=100)  # Increased row height

    for day in sorted_days:
        row = [day] + [matrix[day][slot] for slot in sorted_slots]
        tree.insert('', 'end', values=row)

    # Add scrollbars
    y_scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    x_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

    # Pack everything
    y_scrollbar.pack(side="right", fill="y")
    x_scrollbar.pack(side="bottom", fill="x")
    tree.pack(fill=BOTH, expand=True)

    # Start the main event loop for this window
    root.mainloop()


# Only display if a zero-conflict schedule was found
if z:
    print("Displaying schedule...")  # Debug print
    show_table(z)
else:
    print("No conflict-free schedule was found.")


def display_matrix_table(schedule):
    matrix_window = Toplevel()
    matrix_window.title("Timetable Matrix")

    # Sort days and time slots to ensure consistent order
    sorted_days = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday']
    sorted_slots = ["8:00-10:00", "10:00-12:00", "12:00-2:00", "2:00-4:00", "4:00-6:00"]

    # Create a 2D dictionary: day -> time -> cell content
    matrix = {day: {slot: "" for slot in sorted_slots} for day in sorted_days}
    for prof, course, hours, time, day in schedule:
        cell = f"{prof}\n({course})"
        if matrix[day][time]:  # already something here (conflict, rare with good fitness)
            matrix[day][time] += "\n" + cell
        else:
            matrix[day][time] = cell

    # Treeview setup
    cols = ['Day'] + sorted_slots
    tree = ttk.Treeview(matrix_window, columns=cols, show='headings')
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor='center')

    # Insert each day row
    for day in sorted_days:
        row = [day] + [matrix[day][slot] for slot in sorted_slots]
        tree.insert('', 'end', values=row)

    tree.pack(expand=True, fill='both')
# print(z)


# z=[]
# for p in range(100):
#     y=evolve(y)
#     f=fitness(y)
#     for i in range(len(y)):
#         if fitness(y[i])==0:
#             z=y
#             break
# for i in range(len(y)):
#     if f[i]==0:
#         z.append(y[i])
#         break;


# schedule = z
# # GUI window
# root = tk.Tk()
# root.title("Class Schedule Table")
#
# # Define columns
# columns = ('Professor', 'Course', 'Hours', 'Time', 'Day')
#
# # Create Treeview
# tree = ttk.Treeview(root, columns=columns, show='headings')
# tree.pack(expand=True, fill='both')
#
# # Set column headings
# for col in columns:
#     tree.heading(col, text=col)
#     tree.column(col, anchor='center')
#
# # Insert data into table
# for row in schedule:
#     tree.insert('', tk.END, values=row)
#
# root.mainloop()
#
#


# lst=[40,40,40,40,40]
#
# def individual(length,min,max):
#     return [randint(min,max) for i in range(length)]
#
# member = individual(5,0,100)
# print(member)
# print(sum(member))
#
#
#
# def population(count,length,min,max):
#     return [individual(length,min,max) for i in range(count)]
# print(population(3,5,0,100))
#
#
#
# def fit(indiviual,target):
#     total=sum(indiviual)
#     return abs(total-target)
#
#
# def grade(pop ,target):
#     total_pop=[ fit(x,target) for x in pop]
#     return sum(total_pop)/len(pop)*1.0
#
#
#
#
#
#
# def evolve(pop,target, retain=0.2,random_select=0.05,mutate=0.01):
#     graded =[ (fit(x,target),x) for x in pop]
#     graded=[x[1] for x in sorted(graded)]
#     retain_length=int(len(graded)*retain)
#     parents=graded[:retain_length]
#     for x in graded[retain_length:]:
#         if random_select < random():
#             parents.append(x)
#


# window=Tk()
# window.geometry("720x420")
# window.title("Helwan national university")
# icon=PhotoImage(file='icon2.png')
# window.iconphoto(True,icon)
# window.mainloop()
#








# def fitness(population):
#     conflict_counts = []
#
#     # Iterate over each depth
#     for depth_index, depth in enumerate(population):  # depth_index is for debugging purposes
#         count = 0
#
#
#         # Iterate through rows within the current depth
#         for i, row1 in enumerate(depth):
#             for j, row2 in enumerate(depth[i + 1:], start=i + 1):
#                 if row1[3] == row2[3] and row1[4] == row2[4]:
#
#                     count += 1
#
#         conflict_counts.append(count)
#
#     return conflict_counts


# def evolve(pop, retain=0.2, random_select=0.05, mutate=0.01):
#     # 1. Evaluate fitness
#     fit = fitness(pop)
#     graded = list(zip(pop, fit))
#     graded = sorted(graded, key=lambda x: x[1])  # Sort by fitness (lower = better)
#     sorted_pop = [x[0] for x in graded]
#
#     # 2. Selection (keep top performers + some random)
#     retain_length = int(len(sorted_pop) * retain)
#     parents = sorted_pop[:retain_length]
#
#     # 3. Randomly select some less-fit individuals
#     for individual in sorted_pop[retain_length:]:
#         if random.random() < random_select:
#             parents.append(individual)
#
#
#
#     for individual in parents:
#         if random.random() < mutate:
#             # Pick a random lecture in the schedule
#             lecture_idx = randint(0, len(individual)-1)
#
#             # Change DAY (index 3) and TIME (index 4)
#             individual[lecture_idx][3] = random.choice(days)  # New random day
#             individual[lecture_idx][4] = random.choice(time_slots)  # New random time
#
#     # 5. Crossover (unchanged)
#     parents_length = len(parents)
#     desired_length = len(pop) - parents_length
#     children = []
#
#     while len(children) < desired_length:
#         male_idx = randint(0, parents_length-1)
#         female_idx = randint(0, parents_length-1)
#
#         if male_idx != female_idx:
#             male = parents[male_idx]
#             female = parents[female_idx]
#             crossover_point = randint(1, len(male)-1)
#             child = male[:crossover_point] + female[crossover_point:]
#             children.append(child)
#
#     parents.extend(children)
#     return parents


#
#
#



