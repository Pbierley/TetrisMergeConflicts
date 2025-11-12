from supabase import create_client, Client
from constants import SUPABASE_URL, SUPABASE_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_leaderboard():
    """Fetch top 5 scores from the leaderboard"""
    try:
        response = (
            supabase.table("Leaderboard")
            .select("name, score")
            .order("score", desc=True)
            .limit(5)
            .execute()
        )
        return response.data
    except Exception as e:
        print(f"Error fetching leaderboard: {e}")
        return []


def save_score_to_database(name, score):
    """Save the player's score to the database"""
    try:
        response = (
            supabase.table("Leaderboard")
            .insert({"name": name, "score": score})
            .execute()
        )
        print(f"Score {score} for player '{name}' saved to database!")
        return True
    except Exception as e:
        print(f"Error saving score: {e}")
        return False

