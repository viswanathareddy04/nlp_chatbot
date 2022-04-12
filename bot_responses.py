from models import session, Student, TimeTable, TrainingData, IntentResponse


class BotResponses:
    student_information = dict({s.roll_no: {
        "name": s.name,
        "fee": s.fee,
        "exam": s.exam,
        "grades": "\n".join([f"{grade.subject.name}: {grade.mark}" for grade in s.grades])
    } for s in session.query(Student).all()})

    subjects = dict({
        s.weekday: s.description
        for s in session.query(TimeTable).all()
    })

    data = list([[d.sample, d.index] for d in session.query(TrainingData).all()])

    responses = dict({r.index: {
        "intent": r.intent,
        "response": r.response.split('|')
    } for r in session.query(IntentResponse).all()})
