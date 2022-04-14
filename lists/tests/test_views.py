from django.test import TestCase
from django.urls import reverse
from lists.models import Item, List


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(reverse("view_list", args=[list_.id]))
        self.assertTemplateUsed(response, "list.html")

    def test_passes_correct_list_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(reverse("view_list", args=[correct_list.id]))
        self.assertEqual(response.context["list"], correct_list)

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text="itemey 1", list=correct_list)
        Item.objects.create(text="itemey 2", list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text="other list item 1", list=other_list)
        Item.objects.create(text="other list item 2", list=other_list)

        response = self.client.get(reverse("view_list", args=[correct_list.id]))

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
        self.assertNotContains(response, "other list item 1")
        self.assertNotContains(response, "other list item 2")
        
class NewListTest(TestCase):
    def test_can_save_POST_request(self):
        self.client.post(reverse("new_list"), data={"item_text": "A new list item"})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post(
            reverse("new_list"), data={"item_text": "A new list item"}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, reverse("view_list", args=[new_list.id]))

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post(reverse("new_list"), data={"item_text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "You cannot have an empty list item")
    
    def test_invalid_list_items_arent_saved(self):
        self.client.post(reverse("new_list"), data={"item_text": ""})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)