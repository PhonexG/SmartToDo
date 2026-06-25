from functools import lru_cache

from sentence_transformers import SentenceTransformer, util

from tasks.models import Topic


TOPIC_DESCRIPTIONS = {
    "Programming": "programming, coding, Django, Python, Docker, GitHub, API, database, software development",
    "University": "university, studying, exams, laboratory work, homework, lectures, math, statistics, coursework",
    "English": "English learning, grammar, vocabulary, speaking practice, listening, reading, language study",
    "Music": "music, guitar practice, songs, instruments, chords, solos, rhythm, music theory",
    "Home": "home tasks, cleaning, laundry, room, kitchen, house chores, organizing home",
    "Shopping": "shopping, buying products, ordering food, groceries, market, store, purchases",
    "Health": "health, workout, sleep, doctor, medicine, exercise, mental health, body care",
    "Work": "work tasks, job, meeting, business, project, deadline, client, productivity",
    "General": "general personal tasks, reminders, simple notes, miscellaneous things",
}


def fallback_detect_topic_name(task):
    text = f"{task.title} {task.description}".lower()

    if any(word in text for word in ["django", "python", "docker", "code", "github", "java", "database", "api"]):
        return "Programming"

    if any(word in text for word in ["exam", "lab", "university", "homework", "lecture", "study", "math", "statistics"]):
        return "University"

    if any(word in text for word in ["english", "grammar", "vocabulary", "speaking", "listening", "reading"]):
        return "English"

    if any(word in text for word in ["guitar", "song", "music", "practice", "metallica"]):
        return "Music"

    if any(word in text for word in ["clean", "room", "laundry", "kitchen", "home"]):
        return "Home"

    if any(word in text for word in ["buy", "shop", "order", "market", "food", "milk"]):
        return "Shopping"

    if any(word in text for word in ["workout", "sleep", "doctor", "medicine", "health"]):
        return "Health"

    if any(word in text for word in ["work", "meeting", "client", "job", "business"]):
        return "Work"

    return "General"


@lru_cache(maxsize=1)
def get_model():
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


@lru_cache(maxsize=1)
def get_topic_embeddings():
    model = get_model()

    topic_names = list(TOPIC_DESCRIPTIONS.keys())
    topic_texts = list(TOPIC_DESCRIPTIONS.values())

    topic_embeddings = model.encode(
        topic_texts,
        convert_to_tensor=True
    )

    return topic_names, topic_embeddings


def detect_topic_name_with_ai(task):
    task_text = f"{task.title}. {task.description}".strip()

    if not task_text:
        return "General"

    try:
        model = get_model()
        topic_names, topic_embeddings = get_topic_embeddings()

        task_embedding = model.encode(
            task_text,
            convert_to_tensor=True
        )

        similarity_scores = util.cos_sim(task_embedding, topic_embeddings)[0]

        best_index = int(similarity_scores.argmax())
        best_score = float(similarity_scores[best_index])

        if best_score < 0.25:
            return fallback_detect_topic_name(task)

        return topic_names[best_index]

    except Exception:
        return fallback_detect_topic_name(task)


def assign_topic_to_task(task):
    topic_name = detect_topic_name_with_ai(task)

    topic, created = Topic.objects.get_or_create(
        user=task.user,
        name=topic_name
    )

    task.topic = topic
    task.save(update_fields=["topic"])

    return topic