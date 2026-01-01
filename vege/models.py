from django.db import models
from django.contrib.auth.models import User




class Receipe(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE, null=True)
    receipe_name = models.CharField(max_length=100)
    receipe_description = models.TextField()
    receipe_image = models.ImageField(upload_to="receipe")
    receipe_steps = models.TextField(blank=True, null=True)  #steps of cooking
    receipe_view_count = models.IntegerField(default=1)
    
    def __str__(self):
        return self.receipe_name 
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receipe = models.ForeignKey(Receipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'receipe'], name='unique_user_receipe_like')
        ]
        
    def __str__(self):
        return f"{self.user.username} likes {self.receipe.receipe_name}"
        
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receipe = models.ForeignKey(Receipe, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.receipe.receipe_name}"
    
class ReceipeView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receipe = models.ForeignKey(Receipe, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'receipe'], name='unique_user_receipe_view')
        ]
    def __str__(self):
        return f"{self.user.username}  viewed {self.receipe.receipe_name}"

#this class is use for update the user profile or users information like bio user_profile    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    Profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True, default='default.jpg')
    users_about = models.TextField(blank=True)
    
    def __str__(self):
        return self.user.username
    