import os

# Define the base directory where the templates will be created
base_template_dir = "/Users/Julia/Downloads/braine-package/myapp/templates/myapp/quiz/heritage_quiz"

# Ensure the base directory exists
os.makedirs(base_template_dir, exist_ok=True)

# Questions and their corresponding button texts
questions = [
    ("Where does your income come from right now?", [
        "I’m currently employed full-time.",
        "I run my own small business.",
        "I’m earning from freelance work.",
        "I rely on a pension or retirement income.",
        "I have multiple sources, including investments and side gigs."
    ]),
    ("How does your daily work schedule look?", [
        "I work 9 to 5, Monday through Friday.",
        "I have a flexible schedule, working at different times.",
        "I work part-time, a few hours a day.",
        "I usually work evenings and weekends.",
        "I work freelance, so my schedule changes week to week."
    ]),
    ("What’s making your job harder at the moment?", [
        "I’m struggling with time management and balancing tasks.",
        "Keeping up with new technology is tough for me.",
        "I’m having trouble staying organized at work.",
        "I’m finding it hard to communicate effectively with my team.",
        "I’m facing challenges in learning new skills for my role."
    ]),
    ("How are you doing financially at the moment?", [
        "I’m comfortable but looking to grow my savings.",
        "I’m managing, but I could use more stability.",
        "I’m living paycheck to paycheck.",
        "I’m doing well and saving for future goals.",
        "I’m struggling with debt and trying to improve my situation."
    ]),
    ("How much income would you like to have each year when you retire?", [
        "I’m hoping to have around $50,000 a year in retirement.",
        "I’d like to maintain an income of at least $75,000 per year.",
        "I’m aiming for a comfortable $100,000 a year in retirement.",
        "I’m looking to enjoy $40,000 to $60,000 annually.",
        "I haven’t decided yet, but I want enough to live comfortably."
    ]),
    ("Would you like more freedom to decide how and where you spend your time?", [
        "Yes, having more control over my schedule would be amazing.",
        "Absolutely, I’d love to have the flexibility to work and travel on my own terms.",
        "Definitely, I want the freedom to spend my time how I choose.",
        "For sure, being able to decide when and where I spend my time is important to me.",
        "Yes, flexibility is a priority for me, especially when it comes to balancing work and personal time."
    ]),
    ("Would you like a position where you can focus on the big things, while the small tasks are managed for you?", [
        "Yes, that sounds like an ideal situation for me.",
        "Absolutely, I’d love to focus on the bigger picture without getting bogged down by small tasks.",
        "For sure, it would help me be more productive and focus on what really matters.",
        "Definitely, having the routine stuff managed would make my work much more meaningful.",
        "That would be perfect, allowing me to concentrate on the most important aspects of my job."
    ]),
    ("What would you do with your extra time if you didn’t have to handle all the boring tasks?", [
        "I’d like to spend more time on creative projects and hobbies.",
        "I’d focus on learning new skills and personal development.",
        "I’d dedicate more time to my family and friends.",
        "I’d work on growing my business or side projects.",
        "I’d take more time for self-care and relaxation."
    ]),
    ("Do you want to focus your time on things that align with what you love and care about?", [
        "Yes, I’d love to work on things that inspire me and match my interests.",
        "Absolutely, following my passions is really important to me.",
        "Definitely, I’d love to spend more time doing what I care about most.",
        "For sure, aligning my work with my passions would make me much happier.",
        "Yes, it would be amazing to focus on things that I truly enjoy."
    ]),
    ("How familiar are you with online business opportunities that could improve your lifestyle?", [
        "I’m not very familiar but would love to learn more.",
        "I’ve heard of a few opportunities but haven’t explored them in depth yet.",
        "I know a little and have been considering starting something online.",
        "I’m pretty familiar and have already started looking into some digital business ideas.",
        "I’m very familiar and actively working on growing a digital business."
    ]),
    ("Have you ever turned a hobby or project into extra income, and would you want to keep growing that?", [
        "Yes, I’ve made extra income and would love to grow it further.",
        "I have, and I’m definitely interested in exploring it more.",
        "I haven’t yet, but I’d like to look into making money from my hobbies.",
        "Yes, I’ve earned extra income before and would love to turn it into something bigger.",
        "I’ve thought about it, but I’m not sure how to take it to the next level."
    ]),
    ("How do you feel about learning new skills or trying out new techniques?", [
        "Yes, I’m always excited to learn new things.",
        "I’m open to learning, but it depends on how challenging it is.",
        "I’m comfortable with it, as long as the learning process is straightforward.",
        "I love picking up new skills and expanding my knowledge.",
        "I’m a bit hesitant, but I’m willing to try."
    ]),
    ("Have you tried using any AI tools, and if so, which ones?", [
        "I’ve used AI tools like Siri or Alexa.",
        "I’m familiar with basic AI tools like Google Assistant.",
        "I’ve used AI for photo editing apps like FaceApp.",
        "I’ve heard of AI tools, but I haven’t used any myself.",
        "I’m not familiar with any AI tools yet, but I’m interested in learning."
    ]),
    ("How confident do you feel about your content writing abilities?", [
        "I’m a beginner and still learning the basics.",
        "I have some experience but could improve.",
        "I’m confident but there’s always room to learn more.",
        "I’m quite experienced and feel comfortable writing content.",
        "I’m not familiar with content writing at all."
    ]),
    ("How would you rate your skills in digital marketing?", [
        "I’m a complete beginner and just getting started.",
        "I know a little, but I could use more guidance.",
        "I’m somewhat experienced, but still have a lot to learn.",
        "I’m pretty confident in my digital marketing skills.",
        "I’m not familiar with digital marketing at all."
    ]),
    ("Were you aware that using AI tools can help you make more money?", [
        "No, I didn’t know that! I’d love to learn more.",
        "I’ve heard about it, but I’m not sure how it works.",
        "Yes, I’ve heard AI tools can help with income, but I haven’t tried them yet.",
        "Yes, I know, and I’m already exploring AI to improve my income.",
        "I wasn’t aware, but I’m interested in learning how AI can help."
    ]),
    ("What areas or subjects are you curious about exploring?", [
        "I’m interested in exploring digital marketing.",
        "I’d like to learn more about graphic design.",
        "I’m curious about AI and how it can be applied in different fields.",
        "I want to explore entrepreneurship and starting my own business.",
        "I’m interested in social media management and content creation."
    ]),
    ("How ready do you feel to learn and master AI?", [
        "I’m very ready and excited to start learning AI.",
        "I’m interested but not sure where to start.",
        "I’m somewhat ready but need more guidance.",
        "I’m a bit hesitant but willing to give it a try.",
        "I’m not sure if I’m ready yet, but I’m curious to learn more."
    ]),
    ("Do you find it simple to keep your focus on what you’re doing?", [
        "Yes, I find it easy to stay focused most of the time.",
        "I can focus, but I get distracted sometimes.",
        "It depends on the task—sometimes I find it hard to concentrate.",
        "I struggle to stay focused and often get sidetracked.",
        "I try, but staying focused can be challenging for me."
    ]),
    ("What’s a long-term goal you’d love to achieve?", [
        "I want to start my own business one day.",
        "I’d love to travel the world and explore new places.",
        "I want to learn new skills and become an expert in my field.",
        "I hope to give back to my community through charity work.",
        "I’d like to focus on personal growth and self-development."
    ]),
    ("How much time are you willing to put into reaching your long-term goals?", [
        "I’m willing to dedicate a few hours each week.",
        "I can invest some time daily to work toward my goals.",
        "I’m ready to commit as much time as needed to achieve them.",
        "I’d like to start small but gradually invest more time as I go.",
        "I’m flexible and can adjust my schedule based on the demands of the goal."
    ])
]


# Template content structure
template_structure = '''{{% extends "myapp/quiz/quiz_base.html" %}}
{{% load static %}}
{{% block title %}}{question_title}{{% endblock %}}
{{% block content %}}
{{% include 'myapp/quiz/header.html' %}}
<div class="mobile-container">
    <div class="container text-center mt-4">
        <h2>{question_title}</h2>
        <form method="post">
            {{% csrf_token %}}
            <div class="row justify-content-center">
                {buttons}
            </div>
        </form>
    </div>
</div>

<style>
    .emoji {{
        font-size: 50px;
        margin-right: 15px;
    }}

    .btn-goal {{
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: flex-start;
        width: 100%;
        text-align: left;
        padding: 15px 20px;
        border: none;
        background-color: #f8f9fa;
        border-radius: 10px;
        font-size: 20px;
        transition: background-color 0.3s ease;
    }}

    .btn-goal:hover {{
        background-color: #e2e6ea;
    }}

    .btn-goal span {{
        font-weight: normal;
    }}
</style>
{{% endblock %}}
'''


# Function to create buttons HTML for each option
def create_buttons(options):
    buttons_html = ""
    emoji_list = ["🎯", "🤝", "🛠️", "💪", "🔍"]
    for i, option in enumerate(options):
        buttons_html += f'''
            <div class="col-12 col-md-11 mb-3 mt-3">
                <button type="submit" name="answer" value="{option}" class="btn btn-light btn-goal d-flex align-items-center">
                    <span class="emoji">{emoji_list[i % len(emoji_list)]}</span>
                    <span>{option}</span>
                </button>
            </div>
        '''
    return buttons_html

# Generate templates
for index, (question, options) in enumerate(questions):
    question_title = question
    buttons_html = create_buttons(options)
    template_content = template_structure.format(question_title=question_title, buttons=buttons_html)
    
    # Generate template filename
    template_filename = f"{base_template_dir}/question_{index + 1}.html"
    
    # Write the template content to the file
    with open(template_filename, "w") as file:
        file.write(template_content)

    print(f"Template created: {template_filename}")
