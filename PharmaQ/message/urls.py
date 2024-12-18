from django.urls import path, include

from PharmaQ.message.views import MessageCreateView, SentMessageListView, ReceivedMessageListView, MessageDetailView, \
    MessageDeleteView, ContactUsMessageCreateView

urlpatterns = [
    path('send-to/<int:receiver_pk>/', MessageCreateView.as_view(), name='message-create'),
    path('user/<int:user_pk>/', include([
        path('sent-messages/', SentMessageListView.as_view(), name='sent-message-list'),
        path('received-messages/', ReceivedMessageListView.as_view(), name='received-message-list'),
        path('message/<int:message_pk>/', MessageDetailView.as_view(), name='message-detail'),
        path('delete/<int:message_pk>/', MessageDeleteView.as_view(), name='message-delete' ),
        path('contact-us/', ContactUsMessageCreateView.as_view(), name='contact-us'),
    ])),

]