from frontend.app import create_app
from inderface.face_inder import Face

bantu = Face("Bantu")

bantu.inder()

app = create_app()

app.run(debug=True, host='0.0.0.0', port=5008)
