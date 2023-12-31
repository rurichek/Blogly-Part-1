from unittest import TestCase

from app import app
from models import db, User
# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class PetViewsTestCase(TestCase):
    """Tests for views for Pets."""

    def setUp(self):
        """Add sample pet."""

        User.query.delete()

        user = User(first_name="TestName", last_name="Lucifer", image_url="https://media.newyorker.com/photos/5d0d56a203a303d37b7e4451/4:3/w_1288,h_966,c_limit/Hutton-DevilExpression.jpg")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestName', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>TestName Lucifer</h1>', html)
    
    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "TestName2", "last_name": "Angel", "image_url": "https://static.wikia.nocookie.net/gods_and_demons/images/d/d8/Darren-benton-angel-of-death-2.jpg/revision/latest/scale-to-width-down/1200?cb=20220408063613"}
            resp = client.post("/users/<int:user_id>/edit", data=d, follow_redirects=True)
            # resp = client.get("/users/<int:user_id>")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>TestName2</h1>", html)