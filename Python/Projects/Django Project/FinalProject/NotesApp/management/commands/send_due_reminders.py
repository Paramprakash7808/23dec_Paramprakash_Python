from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import EmailMessage
from NotesApp.models import Note
import datetime


class Command(BaseCommand):
    help = "Send email reminders for notes due within the next 24 hours."

    def handle(self, *args, **options):
        now = timezone.now()
        window_start = now
        window_end = now + datetime.timedelta(hours=24)

        notes_due = Note.objects.filter(
            due_date__gte=window_start,
            due_date__lte=window_end,
            is_deleted=False,
            is_archived=False,
        ).select_related('user')

        sent = 0
        for note in notes_due:
            user = note.user
            if not user.email:
                continue

            time_left = note.due_date - now
            hours_left = int(time_left.total_seconds() // 3600)
            due_str = note.due_date.strftime("%B %d, %Y at %H:%M")

            html = f"""
            <div style="font-family:Arial,sans-serif;max-width:500px;margin:auto;padding:32px;background:#f8fafc;border-radius:12px;">
                <h2 style="color:#f59e0b;">⏰ Upcoming Deadline Reminder</h2>
                <p>Hi <strong>{user.username}</strong>,</p>
                <p>Your note <strong>"{note.title}"</strong> is due in approximately <strong>{hours_left} hour(s)</strong>.</p>
                <div style="background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:16px;margin:16px 0;">
                    <p style="margin:0;font-size:14px;color:#64748b;">Due: <strong style="color:#1e293b;">{due_str}</strong></p>
                </div>
                <p style="color:#64748b;font-size:12px;">Log in to NotesApp to review or update this note.</p>
            </div>
            """
            email_obj = EmailMessage(
                "NotesApp — Due Date Reminder",
                html,
                'no-reply@notesapp.com',
                [user.email]
            )
            email_obj.content_subtype = 'html'
            try:
                email_obj.send()
                sent += 1
                self.stdout.write(self.style.SUCCESS(f"Reminder sent to {user.email} for note '{note.title}'"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to send to {user.email}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"\nDone. {sent} reminder(s) sent."))
