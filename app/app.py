from dbsm import PriorityQueue, HashTable

class ProjectPlan:
    def __init__(self):
        self.priority_queue = PriorityQueue()  # Queue Prioritas
        self.plan_hash = HashTable(size=100)    # Hash untuk penyimpanan informasi tambahan

    def add_plan(self, plan_name, priority, details):
        self.priority_queue.enqueue(plan_name, priority)
        self.plan_hash.insert(plan_name, {'priority': priority, 'details': details})

    def get_next_plan(self):
        next_plan, priority = self.priority_queue.dequeue()
        return next_plan, priority

    def get_plan_details(self, plan_name):
        return self.plan_hash.search(plan_name)

    def get_all_plans(self):
        return self.priority_queue.queue  # Mengambil semua rencana dari queue

def print_menu():
    print("1. Add Plan")
    print("2. Get Next Plan")
    print("3. Get Plan Details")
    print("4. View All Plans")
    print("5. Exit")

def main():
    project_planner = ProjectPlan()

    while True:
        print_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            plan_name = input("Enter plan name: ")
            priority = int(input("Enter priority: "))
            details = input("Enter plan details: ")
            project_planner.add_plan(plan_name, priority, details)
            print("Plan added successfully!")
        elif choice == "2":
            next_plan, priority = project_planner.get_next_plan()
            print(f"Next Plan: {next_plan} with Priority: {priority}")
        elif choice == "3":
            plan_name = input("Enter plan name: ")
            plan_details = project_planner.get_plan_details(plan_name)
            if plan_details:
                print(f"Details for {plan_name}: {plan_details}")
            else:
                print(f"Plan {plan_name} not found.")
        elif choice == "4":
            all_plans = project_planner.get_all_plans()
            if all_plans:
                print("All Plans:")
                for plan in all_plans:
                    print(plan)
            else:
                print("No plans added yet.")
        elif choice == "5":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()