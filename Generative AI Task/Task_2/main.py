from langchain.prompts import PromptTemplate

def define_prompt(student_name, subjects, learning_style, extracurricular_activities, personal_objectives, challenges):
    """
    This function defines the prompt template for creeating study plans for students
    param 'student_name': String full name of student
    param 'subjects': List of strings containing subject names
    param 'learning_style': String containing information about the student's way of learning of the student
    param 'extracurricular_activities': String containing information about the student's extracurricular activities or hobbies
    param 'personal_objectives': String containing information about the student's long-term and/or short-term goals
    param 'challenges': String containing details about the student's perosnal challenges in life that affect their daily tasks
    """
    prompt_template = PromptTemplate(
        input_variables=[
            "student_name", "subjects", 
            "learning_style", "extracurricular_activities", 
            "personal_objectives", "challenges"
        ],
        template = f"""
        You are an educational consultant and expert in creating highly personalized and effective study plans for students. 
        Your task is to design a detailed, individualized study plan for a student based on the following information:

        Student Name: {student_name}
        Subjects and Current Academic Performance: {subjects} (include grades, strengths, and areas for improvement for each subject)
        Preferred Learning Style: {learning_style} (e.g., visual, auditory, kinesthetic, or a combination)
        Extracurricular Activities: {extracurricular_activities} (include activities, time commitments, and skills learned)
        Personal Objectives: {personal_objectives} (e.g., preparing for a specific exam, mastering a subject, or achieving a long-term academic/career goal)
        Challenges: {challenges} (e.g., learning difficulties, time management issues, or any specific obstacles faced by the student)

        Using this information, create a comprehensive study plan that:
        1. Addresses each subject, focusing on improving weaker areas while enhancing strengths.
        2. Incorporates the student's preferred learning style to optimize retention and engagement.
        3. Balances academic priorities with extracurricular commitments, ensuring overall well-being.
        4. Provides specific strategies and resources tailored to the student's challenges and objectives.
        5. Includes actionable, time-bound goals and a weekly schedule for effective time management.

        Format the response as follows:
        1. Overview:
        - A brief summary of the student's profile, goals, and challenges.

        2. Subject-Specific Strategies:
        - Detailed strategies for improving performance in each subject, highlighting specific techniques aligned with the learning style.
        - Suggested resources (e.g., online tools, books, or activities) for each subject.

        3. Extracurricular Integration:
        - Guidance on managing extracurricular activities alongside academics, emphasizing skill transfer where relevant.

        4. Overcoming Challenges:
        - Personalized advice and tools to address the specific challenges faced by the student.

        5. Study Schedule:
        - A detailed weekly schedule, broken into daily activities, with time allocated for each subject, breaks, and extracurricular activities.

        Make the plan motivational, practical, and easy to follow while inspiring the student to achieve their full potential.
        """
    )
    return prompt_template