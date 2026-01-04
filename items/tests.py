from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import RecoveredItem

class ItemViewTests(TestCase):
    def setUp(self):
        img_bytes = (b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
                     b'\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06'
                     b'\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc`\x00\x00\x00\x02\x00\x01'
                     b'\xe2!\xbc3\x00\x00\x00\x00IEND\xaeB`\x82')
        image = SimpleUploadedFile("test.png", img_bytes, content_type="image/png")
        self.item = RecoveredItem.objects.create(
            name="Lost Wallet",
            category="Wallets",
            description="Black leather wallet",
            image=image,
            latitude=12.34,
            longitude=56.78
        )

    def test_item_list_contains_overlay_link(self):
        resp = self.client.get(reverse('item_list'))
        self.assertContains(resp, 'class="card-overlay"')
        self.assertContains(resp, reverse('item_detail', args=[self.item.id]))
        # Accessibility checks
        self.assertContains(resp, 'tabindex="0"')
        self.assertContains(resp, 'aria-label="View details for')
        self.assertContains(resp, 'sr-only')

    def test_item_detail_view(self):
        resp = self.client.get(reverse('item_detail', args=[self.item.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.item.name)
        self.assertContains(resp, 'VIEW ON MAP')
