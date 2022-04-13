from django.test import TestCase
from django.urls import reverse
from lists.models import Item, List


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


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


class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            reverse("add_item", args=[correct_list.id]),
            data={"item_text": "A new item for an existing list"},
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_redirect_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            reverse("add_item", args=[correct_list.id]),
            data={"item_text": "A new item for an existing list"},
        )

        self.assertRedirects(response, reverse("view_list", args=[correct_list.id]))


