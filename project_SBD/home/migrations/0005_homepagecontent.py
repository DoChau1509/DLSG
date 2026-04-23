from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0004_remove_post_category"),
    ]

    operations = [
        migrations.CreateModel(
            name="HomePageContent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("intro_title", models.CharField(default="Giới thiệu lộ trình", max_length=200)),
                (
                    "intro_description",
                    models.TextField(
                        default=(
                            "Lộ trình này được thiết kế đặc biệt dành cho du khách trong nước và quốc tế "
                            "cũng như người dân địa phương mong muốn trải nghiệm nhịp sống trung tâm "
                            "Thành phố Hồ Chí Minh một cách chậm rãi, sâu sắc và thân thiện với môi trường."
                        )
                    ),
                ),
            ],
            options={
                "verbose_name": "Nội dung trang chủ",
                "verbose_name_plural": "Nội dung trang chủ",
            },
        ),
    ]
