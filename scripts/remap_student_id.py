from main.models import Session_subject

def random_numbers_and_letters():
    import random
    import string
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

session_id_list = [9,37,41,42]
#session_id_list = [9]
v=Session_subject.objects.filter(session__id__in=session_id_list).values_list('student_id',flat=True)

student_id_map={}

for i in list(v):
    student_id_map[i]=random_numbers_and_letters()

for i in student_id_map:
    Session_subject.objects.filter(student_id=i).update(student_id=student_id_map[i])
