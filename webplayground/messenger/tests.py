from django.test import TestCase
from django.contrib.auth.models import User
from .models import Thread, Message

# Create your tests here.
class ThreadTestCase(TestCase):
    def setUp(self):
        print("<---!   TEST 1 =  Setup PRINCIPAL")
        #crearemos unos usuarios
        self.user1 = User.objects.create_user('user1', None, 'test1234')
        self.user2 = User.objects.create_user('user2', None, 'test1234')
        self.user3 = User.objects.create_user('user3', None, 'test1234')
        #será TRUE cuando cree sin problemas los usuarios.
        self.thread = Thread.objects.create()
        print("<---!   TEST 1 =  fin\n")


    def test_add_users_to_thread(self):
        print("<---!   TEST 2 =  Al hilo CREADO le asignamos los 2 usuarios al HILO")
        #al hilo le asignamos los 2 usuarios
        self.thread.users.add(self.user1, self.user2)
        #TRUE cuando sea igual a 2
        self.assertEqual(len(self.thread.users.all()), 2)
        print("<---!   TEST 2 =  fin\n")

    def test_filter_thread_by_users(self):
        print("<---!   TEST 3 =  Filtrar hilo por usuarios")
        #recupera un hilo existente a partir de los usuarios...
        print("3 test_filter_thread_by_users")
        #este código se repite porque es idependiente de la función anterior
        self.thread.users.add(self.user1, self.user2)
        #esta es la forma de hacer un SELECT
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2)
        #si es VERDAD!!...cuando lo devuelve en la primera posición
        self.assertEqual(self.thread, threads[0])
        print("<---!   TEST 3 =  fin\n")

    def test_filter_non_existent_thread(self):
        print("<---!   TEST 4 = de no crear usuarios, debe mandar 0 hilos")
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2)
        #en esta caso el valor esperado es 0 HILOS
        self.assertEqual(len(threads), 0) 
        print("<---!   TEST 4 =  fin\n")

    def test_add_messages_to_thread(self):
        print("<---!   TEST 5 =  Adicionar un mensaje en la conversación")
        self.thread.users.add(self.user1, self.user2)
        message1 = Message.objects.create(user=self.user1, content="Muy buenas")
        message2 = Message.objects.create(user=self.user2, content="Hola")
        self.thread.messages.add(message1, message2)
        
        #TRUE si hay solamente en este hilo 2 mensajes
        self.assertEqual(len(self.thread.messages.all()), 2)
        print("<---!   TEST 5 =  fin\n")


        print("<---!   TEST 5 =  Chismear\n")
        for message in self.thread.messages.all():
            print("({}): {}".format(message.user, message.content))
        print("<---!   TEST 5 =  fin\n")

    def test_add_message_from_user_not_in_thread(self):
        print("<---!   TEST 6 =  Adicionar un mensaje de un usuario que no esta en la conversación")
        self.thread.users.add(self.user1, self.user2)
        message1 = Message.objects.create(user=self.user1, content="Muy buenas")
        message2 = Message.objects.create(user=self.user2, content="Hola")
        message3 = Message.objects.create(user=self.user3, content="Soy un espía")
        self.thread.messages.add(message1, message2, message3)
        self.assertEqual(len(self.thread.messages.all()), 2)
        print("<---!   TEST 6 =  fin\n")

    def test_find_thread_with_custom_manager(self):
        print("7 test_find_thread_with_custom_manager")
        self.thread.users.add(self.user1, self.user2)
        thread = Thread.objects.find(self.user1,self.user2)
        self.assertEqual(self.thread, thread)
        print("<---!   TEST 7 =  fin\n")
    def test_find_or_create_thread_with_custom_manager(self):
        print("8 test_find_thread_with_custom_manager")
        
        self.thread.users.add(self.user1, self.user2)
        thread = Thread.objects.find_or_create(self.user1,self.user2)
        self.assertEqual(self.thread, thread)    
        thread = Thread.objects.find_or_create(self.user1,self.user3)
        self.assertIsNotNone(thread)       
        print("<---!   TEST 8 =  fin\n")

