from tasks.models import Topic


def detect_topic_name(task):
    text = f"{task.title} {task.description}".lower()

    programming_keywords = [
        "django", "python", "docker", "github", "code", "programming",
        "java", "c++", "api", "database", "mysql"
    ]

    university_keywords = [
        "exam", "lab", "university", "statistics", "math", "lecture",
        "homework", "course", "study"
    ]

    home_keywords = [
        "clean", "room", "kitchen", "laundry", "home"
    ]

    shopping_keywords = [
        "buy", "shop", "order", "food", "milk", "market"
    ]

    english_keywords = [
        "english", "grammar", "vocabulary", "speaking", "listening"
    ]

    music_keywords = [
        "guitar", "song", "metallica", "music", "practice"
    ]

    if any(word in text for word in programming_keywords):
        return "Programming"

    if any(word in text for word in university_keywords):
        return "University"

    if any(word in text for word in home_keywords):
        return "Home"

    if any(word in text for word in shopping_keywords):
        return "Shopping"

    if any(word in text for word in english_keywords):
        return "English"

    if any(word in text for word in music_keywords):
        return "Music"

    return "General"


def assign_topic_to_task(task):
    topic_name = detect_topic_name(task)

    topic, created = Topic.objects.get_or_create(
        user=task.user,
        name=topic_name
    )

    task.topic = topic
    task.save(update_fields=["topic"])

    return topic