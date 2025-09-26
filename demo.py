import os
from supabase import create_client, Client

SUPABASE_URL="https://ddafhennccnnqlzdaxer.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRkYWZoZW5uY2NubnFsemRheGVyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg3MzkxMjUsImV4cCI6MjA3NDMxNTEyNX0.iBn49djWQBUkoyJ6dXFD9g02oNibyhU8XRCEpNFQCtM"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

#add a new row to the leaderboard table
response = (
    supabase.table("Leaderboard")
    .insert({"name": "Test User", "score": 100})
    .execute()
)
#update a row in the instruments table
response = (
    supabase.table("Leaderboard")
    .update({"name": "Test_User", "score": 150})
    .eq("id", 4)
    .execute()
)

#delete a row in the instruments table
response = (
    supabase.table("Leaderboard")
    .delete()
    .eq("id", 4)
    .execute()
)

results = supabase.table("Leaderboard").select("*").execute()
print(results)
