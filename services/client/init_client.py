from models import Base, Client
from database import engine, SessionLocal
from passlib.hash import bcrypt

def init_db():
    # Créer les tables
    Base.metadata.create_all(bind=engine)

    # Créer une session
    db = SessionLocal()

    # Données à insérer
    clients = [
        {
            "nom": "Dupont",
            "prenom": "Alice",
            "email": "alice.dupont@example.com",
            "mot_de_passe": "password123",
            "adresse": "123 rue Principale",
            "telephone": "514-123-4567"
        },
        {
            "nom": "Lefebvre",
            "prenom": "Jean",
            "email": "jean.lefebvre@example.com",
            "mot_de_passe": "secret456",
            "adresse": "456 avenue Laval",
            "telephone": "438-987-6543"
        }
    ]

    for c in clients:
        existing = db.query(Client).filter_by(email=c["email"]).first()
        if not existing:
            hashed_pw = bcrypt.hash(c["mot_de_passe"])
            client = Client(
                nom=c["nom"],
                prenom=c["prenom"],
                email=c["email"],
                mot_de_passe=hashed_pw,
                adresse=c["adresse"],
                telephone=c["telephone"]
            )
            db.add(client)

    db.commit()
    db.close()
    print("✅ Données clients initialisées.")

if __name__ == "__main__":
    init_db()
