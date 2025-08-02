from django.core.management.base import BaseCommand
from core.soru_uretici import SoruUretici

class Command(BaseCommand):
    help = 'Belirtilen bir konu (Topic) için belirtilen sayıda soru üretir.'

    def add_arguments(self, parser):
        parser.add_argument('topic_id', type=int, help='Soruların üretileceği konunun ID\'si.')
        parser.add_argument(
            '--count',
            type=int,
            default=1,
            help='Üretilecek toplam soru sayısı. Varsayılan: 1'
        )

    def handle(self, *args, **options):
        topic_id = options['topic_id']
        count = options['count']
        
        uretici = SoruUretici()
        
        self.stdout.write(self.style.SUCCESS(
            f"'{topic_id}' ID'li konu için {count} adet soru üretme işlemi başlıyor..."
        ))
        
        basarili_sayisi = 0
        for i in range(count):
            self.stdout.write(f"Soru {i+1}/{count} üretiliyor...")
            if uretici.generate_and_save_question(topic_id):
                basarili_sayisi += 1

        self.stdout.write(self.style.SUCCESS(
            f"İşlem tamamlandı! Toplam {basarili_sayisi} adet yeni soru başarıyla oluşturuldu."
        ))