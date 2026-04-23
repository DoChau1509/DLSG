from django.db import models

class ProjectCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.PROTECT,
        related_name='projects',
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        related_name='products',
    )

    def __str__(self):
        return self.name


# 11/4/2026: Hoàng
class PostCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class HomePageContent(models.Model):
    intro_title = models.CharField(max_length=200, default="Giới thiệu lộ trình")
    intro_description = models.TextField(
        default=(
            "Lộ trình này được thiết kế đặc biệt dành cho du khách trong nước và quốc tế "
            "cũng như người dân địa phương mong muốn trải nghiệm nhịp sống trung tâm "
            "Thành phố Hồ Chí Minh một cách chậm rãi, sâu sắc và thân thiện với môi trường."
        )
    )

    class Meta:
        verbose_name = "Nội dung trang chủ"
        verbose_name_plural = "Nội dung trang chủ"

    def __str__(self):
        return "Nội dung giới thiệu trang chủ"
    
class Target(models.Model):
    intro_title = models.CharField(max_length=200, default="Mục tiêu và Giá trị")
    intro_description = models.TextField(
        default=(
           "Lộ trình góp phần giảm tải áp lực giao thông và ô nhiễm không khí tại khu vực trung tâm thành phố – một trong những vấn đề cấp thiết của đô thị lớn. Đồng thời, nó khuyến khích du khách và người dân khám phá Sài Gòn theo cách chậm rãi và gần gũi, tận hưởng không gian công cộng, di sản lịch sử và văn hóa sống động thông qua phương thức di chuyển bền vững. Đây không chỉ là một hành trình du lịch thông thường mà còn là trải nghiệm giáo dục, giúp nâng cao ý thức bảo vệ môi trường và nuôi dưỡng tình yêu dành cho thành phố."
        )
    )

    class Meta:
        verbose_name = "Mục tiêu và Giá trị"
        verbose_name_plural = "Mục tiêu và Giá trị"

    def __str__(self):
        return "Nội dung mục tiêu và giá trị trang chủ"

class CusObj(models.Model):
    intro_title = models.CharField(max_length=200, default="Đối tượng phù hợp")
    intro_description = models.TextField(
        default=(
           "Lộ trình phù hợp với học sinh, sinh viên, giới trẻ, cặp đôi và nhóm bạn đang tìm kiếm một ngày trải nghiệm vừa thư giãn, vừa giàu giá trị văn hóa và môi trường. Với cách di chuyển nhẹ nhàng, chi phí hợp lý và tính linh hoạt cao, lộ trình này đặc biệt dễ thực hiện đối với những người yêu thích du lịch trải nghiệm, slow travel và các hoạt động thân thiện với thiên nhiên."
        )
    )

    class Meta:
        verbose_name = "Đối tượng phù hợp"
        verbose_name_plural = "Đối tượng phù hợp"

    def __str__(self):
        return "Nội dung đối tượng phù hợp trang chủ"
    
class QnA(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Câu hỏi thường gặp"
        verbose_name_plural = "Câu hỏi thường gặp"

    def __str__(self):
        return self.question
