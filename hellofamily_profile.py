from hellofamily import app
from app.topic.views import profile
import cProfile
from pstats import Stats


def profile_request(path, cookie, f):
    pr = cProfile.Profile()
    headers = {'Cookie': cookie}

    with app.test_request_context(path, headers=headers):
        pr.enable()
        f()

        pr.disable()

    pr.create_stats()
    s = Stats(pr).sort_stats('cumulative')
    s.dump_stats('profile.pstat')

    s.print_stats('.*hellofamily.*')


if __name__ == '__main__':
    path = '/topic/profile'
    cookie = 'remember_token=1|fedaae9a15f1b7a1e8c1c7167144fdcb262af7e6dad4fa1f308c8031ddd7e5f9d261714700dc6279e212c85c9cc9cf4f1756fe06c71f55c438d6f606dd6a13c3; session=eyJfZnJlc2giOmZhbHNlLCJjc3JmX3Rva2VuIjoiYzVlNWM3MWI2MjkwYjQ4MjNhNGMxMjY5NDQ5YjAwMmFhYzE5MmEyOSIsInVzZXJfaWQiOiIxIn0.XTpkOg.CIwOzik004-l4UWqp6xRRoQmwxo'
    profile_request(path, cookie, profile)