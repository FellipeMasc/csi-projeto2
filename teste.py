from whatsapp import WhatsApp

app = WhatsApp(100)

# app.send_message("Safadão T26", "oi")

participants = app.get_group_participants("Computos 26")

print(participants)