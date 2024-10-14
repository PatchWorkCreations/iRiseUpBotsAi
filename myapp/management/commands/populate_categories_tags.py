from django.core.management.base import BaseCommand
from myapp.models import Category, Tag

class Command(BaseCommand):
    help = 'Populate categories and tags for the iRiseUp Academy website'

    def handle(self, *args, **kwargs):
        categories = [
            "Entrepreneurship", "Digital Marketing", "Virtual Assistance",
            "AI for Business", "Content Creation", "Graphic Design",
            "Web Development", "Social Media Management", "E-Commerce and Online Sales",
            "Podcasting", "Online Tutoring", "Consulting and Coaching", "Permaculture",
            "Career Development", "Personal Branding", "Advanced Permaculture"
        ]

        tags = [
            "Leadership", "Side Hustles", "Work from Home", "Freelancing",
            "Small Business", "Digital Transformation", "SEO Strategies", "Social Media Tips",
            "Email Marketing", "Video Editing", "Content Writing", "Customer Service",
            "Remote Jobs", "Passive Income", "Branding Tips", "Productivity Hacks",
            "Sustainability", "Organic Farming", "Retirement Jobs", "Career Shift"
        ]

        for category in categories:
            Category.objects.get_or_create(name=category)

        for tag in tags:
            Tag.objects.get_or_create(name=tag)

        self.stdout.write(self.style.SUCCESS('Successfully populated categories and tags'))
