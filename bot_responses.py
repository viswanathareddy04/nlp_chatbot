
class BotResponses:

    student_information = {
        "C01": {
            "name": "John",
            "exam": "April 14, 2022",
            "grades": "CBD: 89%\nALML:95%",
            "fee": "$200",
        },
        "C02": {
            "name": "Dan",
            "exam": "April 14, 2022",
            "grades": "CBD: 90%\nALML:95%",
            "fee": "$100",
        },
        "C03": {
            "name": "Michelle",
            "exam": "April 14, 2022",
            "grades": "CBD: 79%\nALML:95%",
            "fee": "$150",
        },
        "C04": {
            "name": "Rosi",
            "exam": "April 14, 2022",
            "grades": "CBD: 84%\nALML:95%",
            "fee": "$230",

        }
    }

    subjects = {"Monday": "Into to AI at 1:00 PM to 4.30 PM", "Tuesday": "CBD at 12:30 PM to 4.30 PM",
                "Wednesday": "Python at 12:30 PM to 4.30 PM", "Thursday": "DS at 08:00 AM to 12.30 PM", "Friday": "Communication at 11.30 AM to 4:00 PM"}

    data = [
        ["Hi", 0], ["Hello", 0], ["Hey", 0], ["Heya", 0],
        ["Goodbye", 9], ["Byebye", 9], ["Bye", 9],
        ["Thanku", 10], ["Thank You", 10], ["Thanks", 10], [
            "Thanks a lot", 10], ["Thank you very much", 10],
        ["Thank you so much", 10],
        ["grade", 11], ['grades', 11], ['marks', 11],
        ["fee", 12], ['college fee', 12], ['semester fee', 12],
        ["subject time", 14], ['class time', 14], [
            'today class time', 14], ['today subject class time', 14],
        ["final exam date", 13], ['exam date', 13], ['semester date', 13],
    ]

    responses = {
        0: {"intent": "greetings", "response": ['Hi Dear', 'Hi', 'Hello', 'Nice to see you', ]},
        1: {"intent": "studentid", "response": ['Welcome to Lambton {username}!']},
        11: {"intent": "grade", "response": ['Hi {username}, your grades are as follows\n {grades}']},
        12: {"intent": "fee", "response": ['Hi {username}, your total college_fee is {college_fee}. Please visit this URL to pay the fee https://www.lambtoncollege.ca/custom/LambtonApps/Payments/SecurePay.aspx']},
        13: {"intent": "date", "response": ['Hi {username}, your exam date is {exam_date}']},
        14: {"intent": "time", "response": ['Hi {username}, {class_subj} . ']},
        9: {"intent": "goodbye", "response": ['Goodbye', 'Byebye', 'Bye', 'Have a good day']},
        10: {"intent": "thankyou",
             "response": ['You\'re welcome.', 'No problem.', 'No worries.', ' My pleasure.', 'Glad to help.']}}
