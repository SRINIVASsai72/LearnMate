import tkinter as tk
import wikipediaapi

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Generator")

        self.topic_label = tk.Label(root, text="Enter Topic:")
        self.topic_label.pack(pady=5)

        self.topic_entry = tk.Entry(root)
        self.topic_entry.pack(pady=5)

        self.start_button = tk.Button(root, text="Start Quiz", command=self.start_quiz)
        self.start_button.pack(pady=10)

        self.quiz_frame = None
        self.questions = []
        self.current_question_index = 0
        self.score = 0

    def fetch_content(self, topic):
        # Specify user agent
        wiki_wiki = wikipediaapi.Wikipedia(
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent='MyQuizApp/1.0 (https://yourwebsite.com; your_email@example.com)'
        )
        page = wiki_wiki.page(topic)

        if page.exists():
            return page.summary
        else:
            return None

    def generate_questions(self, topic):
        content = self.fetch_content(topic)

        if content:
            # Here we create simple questions based on the content
            sentences = content.split('.')
            questions = [f"What is {sentence.strip()}?" for sentence in sentences if sentence]
            return questions[:5]  # Get the first 5 questions
        else:
            return []

    def start_quiz(self):
        topic = self.topic_entry.get()
        self.questions = self.generate_questions(topic)

        if self.quiz_frame:
            self.quiz_frame.destroy()

        self.current_question_index = 0
        self.score = 0

        self.quiz_frame = tk.Frame(self.root)
        self.quiz_frame.pack(pady=10)

        if self.questions:
            self.question_label = tk.Label(self.quiz_frame, text=self.questions[self.current_question_index])
            self.question_label.pack(pady=5)

            self.answer_entry = tk.Entry(self.quiz_frame)
            self.answer_entry.pack(pady=5)

            self.submit_button = tk.Button(self.quiz_frame, text="Submit Answer", command=self.submit_answer)
            self.submit_button.pack(pady=10)
        else:
            self.question_label = tk.Label(self.quiz_frame, text="No questions found.")
            self.question_label.pack(pady=5)

    def submit_answer(self):
        answer = self.answer_entry.get()
        # Here you could validate the answer; for demo purposes, we increment the score
        self.score += 1  # Replace this with actual answer validation

        self.current_question_index += 1

        if self.current_question_index < len(self.questions):
            self.question_label.config(text=self.questions[self.current_question_index])
            self.answer_entry.delete(0, tk.END)
        else:
            self.finish_quiz()

    def finish_quiz(self):
        self.quiz_frame.destroy()
        result_frame = tk.Frame(self.root)
        result_frame.pack(pady=10)

        result_label = tk.Label(result_frame, text=f"You scored {self.score} out of {len(self.questions)}")
        result_label.pack(pady=5)

        restart_button = tk.Button(result_frame, text="Restart", command=self.restart_quiz)
        restart_button.pack(pady=10)

    def restart_quiz(self):
        if self.quiz_frame:
            self.quiz_frame.destroy()
        self.topic_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
