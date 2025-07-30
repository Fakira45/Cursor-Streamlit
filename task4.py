import streamlit as st
import random
import datetime
from typing import List, Dict, Optional
import base64
from PIL import Image, ImageDraw, ImageFont
import io

class InstagramApp:
    def __init__(self):
        self.users = {
            "john_doe": {
                "name": "John Doe",
                "bio": "Photography enthusiast 📸",
                "followers": 1250,
                "following": 890,
                "posts": 45,
                "profile_pic": "👨‍💼"
            },
            "jane_smith": {
                "name": "Jane Smith",
                "bio": "Travel lover ✈️ | Food blogger 🍕",
                "followers": 2340,
                "following": 567,
                "posts": 78,
                "profile_pic": "👩‍💼"
            },
            "mike_wilson": {
                "name": "Mike Wilson",
                "bio": "Fitness coach 💪 | Healthy living",
                "followers": 890,
                "following": 234,
                "posts": 32,
                "profile_pic": "🏃‍♂️"
            },
            "sarah_jones": {
                "name": "Sarah Jones",
                "bio": "Artist 🎨 | Creative soul",
                "followers": 1567,
                "following": 445,
                "posts": 56,
                "profile_pic": "👩‍🎨"
            }
        }
        
        self.posts = [
            {
                "id": 1,
                "username": "john_doe",
                "image": "🌅",
                "caption": "Beautiful sunset at the beach! #sunset #beach #photography",
                "likes": 234,
                "comments": [
                    {"username": "jane_smith", "text": "Amazing shot! 🔥", "time": "2h ago"},
                    {"username": "mike_wilson", "text": "Love this! 😍", "time": "1h ago"}
                ],
                "time": "3h ago",
                "location": "Miami Beach, FL"
            },
            {
                "id": 2,
                "username": "jane_smith",
                "image": "🍕",
                "caption": "Best pizza in town! 🍕 #food #pizza #delicious",
                "likes": 456,
                "comments": [
                    {"username": "john_doe", "text": "Looks delicious! 😋", "time": "30m ago"},
                    {"username": "sarah_jones", "text": "Where is this? 🤔", "time": "15m ago"}
                ],
                "time": "1h ago",
                "location": "Pizza Palace, NYC"
            },
            {
                "id": 3,
                "username": "mike_wilson",
                "image": "💪",
                "caption": "Morning workout complete! 💪 #fitness #workout #motivation",
                "likes": 189,
                "comments": [
                    {"username": "john_doe", "text": "Keep it up! 💪", "time": "45m ago"},
                    {"username": "jane_smith", "text": "Inspiring! 🔥", "time": "20m ago"}
                ],
                "time": "2h ago",
                "location": "Gym Central"
            },
            {
                "id": 4,
                "username": "sarah_jones",
                "image": "🎨",
                "caption": "New artwork in progress! 🎨 #art #creative #painting",
                "likes": 567,
                "comments": [
                    {"username": "jane_smith", "text": "Stunning! 😍", "time": "1h ago"},
                    {"username": "mike_wilson", "text": "Beautiful work! 👏", "time": "30m ago"}
                ],
                "time": "4h ago",
                "location": "Studio Art"
            }
        ]
        
        self.stories = [
            {"username": "john_doe", "image": "🌅", "time": "2h ago"},
            {"username": "jane_smith", "image": "🍕", "time": "1h ago"},
            {"username": "mike_wilson", "image": "💪", "time": "30m ago"},
            {"username": "sarah_jones", "image": "🎨", "time": "15m ago"}
        ]
        
        self.current_user = "john_doe"
        self.liked_posts = set()
        self.following = {"jane_smith", "mike_wilson"}
        
    def like_post(self, post_id: int):
        """Like or unlike a post"""
        if post_id in self.liked_posts:
            self.liked_posts.remove(post_id)
            # Decrease likes
            for post in self.posts:
                if post["id"] == post_id:
                    post["likes"] -= 1
                    break
        else:
            self.liked_posts.add(post_id)
            # Increase likes
            for post in self.posts:
                if post["id"] == post_id:
                    post["likes"] += 1
                    break
                    
    def add_comment(self, post_id: int, comment_text: str):
        """Add a comment to a post"""
        for post in self.posts:
            if post["id"] == post_id:
                new_comment = {
                    "username": self.current_user,
                    "text": comment_text,
                    "time": "Just now"
                }
                post["comments"].append(new_comment)
                break
                
    def follow_user(self, username: str):
        """Follow or unfollow a user"""
        if username in self.following:
            self.following.remove(username)
            self.users[username]["followers"] -= 1
        else:
            self.following.add(username)
            self.users[username]["followers"] += 1
            
    def create_post(self, image: str, caption: str, location: str = ""):
        """Create a new post"""
        new_post = {
            "id": len(self.posts) + 1,
            "username": self.current_user,
            "image": image,
            "caption": caption,
            "likes": 0,
            "comments": [],
            "time": "Just now",
            "location": location
        }
        self.posts.insert(0, new_post)
        self.users[self.current_user]["posts"] += 1

# Initialize session state
if 'instagram_app' not in st.session_state:
    st.session_state.instagram_app = InstagramApp()

app = st.session_state.instagram_app

# Streamlit UI
st.set_page_config(page_title="Instagram Clone", layout="wide")

# Custom CSS for Instagram-like styling
st.markdown("""
<style>
.instagram-container {
    background: linear-gradient(45deg, #f09433 0%,#e6683c 25%,#dc2743 50%,#cc2366 75%,#bc1888 100%);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
}

.post-container {
    background: white;
    border-radius: 10px;
    padding: 20px;
    margin: 20px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.story-container {
    background: white;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 10px;
    border: 3px solid #e6683c;
}

.user-profile {
    background: white;
    border-radius: 10px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.like-button {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    transition: transform 0.2s;
}

.like-button:hover {
    transform: scale(1.2);
}

.comment-section {
    background: #f8f9fa;
    border-radius: 10px;
    padding: 15px;
    margin-top: 15px;
}

.navbar {
    background: white;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.sidebar {
    background: white;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# Navigation
st.markdown('<div class="navbar">', unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown("### 📱 Instagram Clone")
with col2:
    if st.button("🏠 Home"):
        st.session_state.page = "home"
with col3:
    if st.button("🔍 Explore"):
        st.session_state.page = "explore"
with col4:
    if st.button("➕ Create"):
        st.session_state.page = "create"
with col5:
    if st.button("👤 Profile"):
        st.session_state.page = "profile"
st.markdown('</div>', unsafe_allow_html=True)

# Initialize page
if 'page' not in st.session_state:
    st.session_state.page = "home"

# Main content based on page
if st.session_state.page == "home":
    # Stories section
    st.markdown("### 📖 Stories")
    story_cols = st.columns(len(app.stories))
    for i, story in enumerate(app.stories):
        with story_cols[i]:
            st.markdown(f'<div class="story-container">{story["image"]}</div>', unsafe_allow_html=True)
            st.write(f"@{story['username']}")
            st.write(story["time"])
    
    # Posts feed
    st.markdown("### 📱 Posts Feed")
    for post in app.posts:
        with st.container():
            st.markdown('<div class="post-container">', unsafe_allow_html=True)
            
            # Post header
            col1, col2, col3 = st.columns([1, 3, 1])
            with col1:
                st.write(f"{app.users[post['username']]['profile_pic']}")
            with col2:
                st.write(f"**{app.users[post['username']]['name']}**")
                if post.get('location'):
                    st.write(f"📍 {post['location']}")
            with col3:
                st.write("⋮")
            
            # Post image
            st.markdown(f"<h2 style='text-align: center; font-size: 48px;'>{post['image']}</h2>", unsafe_allow_html=True)
            
            # Post actions
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button(f"{'❤️' if post['id'] in app.liked_posts else '🤍'}", key=f"like_{post['id']}"):
                    app.like_post(post['id'])
                    st.rerun()
            with col2:
                st.button("💬", key=f"comment_{post['id']}")
            with col3:
                st.button("📤", key=f"share_{post['id']}")
            with col4:
                st.button("🔖", key=f"save_{post['id']}")
            
            # Likes count
            st.write(f"**{post['likes']} likes**")
            
            # Caption
            st.write(f"**{app.users[post['username']]['name']}** {post['caption']}")
            
            # Comments
            if post['comments']:
                st.write("**Comments:**")
                for comment in post['comments'][:3]:  # Show first 3 comments
                    st.write(f"**{app.users[comment['username']]['name']}** {comment['text']}")
                if len(post['comments']) > 3:
                    st.write(f"View all {len(post['comments'])} comments")
            
            # Add comment
            comment_text = st.text_input("Add a comment...", key=f"comment_input_{post['id']}")
            if st.button("Post", key=f"post_comment_{post['id']}"):
                if comment_text:
                    app.add_comment(post['id'], comment_text)
                    st.rerun()
            
            st.write(f"*{post['time']}*")
            st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "explore":
    st.markdown("### 🔍 Explore")
    
    # Search bar
    search_query = st.text_input("Search users...")
    
    # User suggestions
    st.markdown("### 👥 Suggested Users")
    for username, user_data in app.users.items():
        if username != app.current_user:
            with st.container():
                st.markdown('<div class="user-profile">', unsafe_allow_html=True)
                col1, col2, col3 = st.columns([1, 3, 1])
                with col1:
                    st.write(f"{user_data['profile_pic']}")
                with col2:
                    st.write(f"**{user_data['name']}**")
                    st.write(f"@{username}")
                    st.write(user_data['bio'])
                with col3:
                    if username in app.following:
                        if st.button("Unfollow", key=f"unfollow_{username}"):
                            app.follow_user(username)
                            st.rerun()
                    else:
                        if st.button("Follow", key=f"follow_{username}"):
                            app.follow_user(username)
                            st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "create":
    st.markdown("### ➕ Create New Post")
    
    # Post creation form
    with st.form("create_post"):
        st.write("**Upload Image**")
        image_options = ["🌅", "🍕", "💪", "🎨", "🏖️", "🍔", "🏃‍♂️", "🎭", "🌺", "🏔️"]
        selected_image = st.selectbox("Choose an image:", image_options)
        
        caption = st.text_area("Write a caption...", placeholder="What's on your mind?")
        location = st.text_input("Add location (optional)")
        
        if st.form_submit_button("Share Post"):
            if caption:
                app.create_post(selected_image, caption, location)
                st.success("Post created successfully!")
                st.session_state.page = "home"
                st.rerun()
            else:
                st.error("Please add a caption!")

elif st.session_state.page == "profile":
    st.markdown("### 👤 Profile")
    
    current_user_data = app.users[app.current_user]
    
    # Profile header
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(f"<h1 style='font-size: 48px;'>{current_user_data['profile_pic']}</h1>", unsafe_allow_html=True)
    with col2:
        st.write(f"**{current_user_data['name']}**")
        st.write(f"@{app.current_user}")
        st.write(current_user_data['bio'])
        
        # Stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**{current_user_data['posts']}** posts")
        with col2:
            st.write(f"**{current_user_data['followers']}** followers")
        with col3:
            st.write(f"**{current_user_data['following']}** following")
        
        if st.button("Edit Profile"):
            st.write("Profile editing feature coming soon!")
    
    # User's posts
    st.markdown("### 📸 Posts")
    user_posts = [post for post in app.posts if post['username'] == app.current_user]
    
    if user_posts:
        # Create a grid layout for posts
        cols = st.columns(3)
        for i, post in enumerate(user_posts):
            with cols[i % 3]:
                st.markdown(f"<h2 style='text-align: center; font-size: 36px;'>{post['image']}</h2>", unsafe_allow_html=True)
                st.write(f"❤️ {post['likes']} likes")
                st.write(f"💬 {len(post['comments'])} comments")
    else:
        st.write("No posts yet. Create your first post!")

# Sidebar with suggestions
with st.sidebar:
    st.markdown('<div class="sidebar">', unsafe_allow_html=True)
    st.markdown("### 👥 Suggestions for You")
    
    for username, user_data in app.users.items():
        if username != app.current_user and username not in app.following:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.write(f"{user_data['profile_pic']}")
            with col2:
                st.write(f"**{user_data['name']}**")
                st.write(f"@{username}")
                if st.button("Follow", key=f"sidebar_follow_{username}"):
                    app.follow_user(username)
                    st.rerun()
    
    st.markdown("### 📱 Quick Actions")
    if st.button("🔄 Refresh Feed"):
        st.rerun()
    if st.button("📊 View Analytics"):
        st.write("Analytics feature coming soon!")
    if st.button("⚙️ Settings"):
        st.write("Settings feature coming soon!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
### 🎯 Instagram Clone Features:
- **📱 Posts Feed**: Like, comment, and share posts
- **📖 Stories**: View user stories
- **👥 User Profiles**: Follow/unfollow users
- **➕ Create Posts**: Share your moments
- **🔍 Explore**: Discover new users
- **💬 Comments**: Add comments to posts
- **❤️ Likes**: Like and unlike posts
- **📊 User Stats**: Followers, following, posts count

### 🎮 How to Use:
1. **Home**: View posts feed and stories
2. **Explore**: Discover and follow new users
3. **Create**: Share new posts with captions
4. **Profile**: View your profile and posts
5. **Sidebar**: Quick actions and suggestions

### 🔧 Special Features:
- **Responsive Design**: Works on different screen sizes
- **Instagram-like UI**: Beautiful gradient design
- **Real-time Interactions**: Like, comment, follow instantly
- **User Management**: Follow/unfollow functionality
- **Post Creation**: Add images, captions, and locations
""")
