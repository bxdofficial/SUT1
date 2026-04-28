"""
بيانات أولية للموقع - شخصيات، خدمات، معرض، شهادات
يتم تشغيله مرة واحدة لملء قاعدة البيانات.
"""
from sqlalchemy.orm import Session
import bcrypt
from .database import SessionLocal, engine, Base
from . import models


def hash_password(plain: str) -> str:
    """تشفير كلمة المرور باستخدام bcrypt مباشرة"""
    return bcrypt.hashpw(plain.encode("utf-8")[:72], bcrypt.gensalt()).decode("utf-8")


# ============ روابط الصور (مأخوذة من بحث صور احترافي) ============

CHARACTERS_DATA = [
    {
        "name_ar": "سبونج بوب",
        "name_en": "SpongeBob",
        "slug": "spongebob",
        "description": "الإسفنجة الصفراء الشهيرة من قاع البحر، مرحة وضاحكة وتجعل الأطفال يستمتعون بكل دقيقة!",
        "image_url": "https://sspark.genspark.ai/cfimages?u1=Vs%2FhLzidWSNfinSpigNVuNH4aeVweFuTF4gEfM2QqjJaYjB65Vyakkq9l0bbcA2kwOMPIwaNhgd2bv2rO5Lg%2BJGqS4ul3%2BiLYqa%2FB8ILcB124eP6SZNiUFDC%2FArKIJ4m%2FYR5ddRqLJsoruRscKqGstvGcLOkiXnd&u2=mhTAJdgPB9TvZC4p&width=2560",
        "category": "cartoon",
        "price_per_hour": 600,
        "color_theme": "#FFE66D",
        "is_featured": True,
    },
    {
        "name_ar": "إلسا - فروزن",
        "name_en": "Elsa - Frozen",
        "slug": "elsa",
        "description": "الأميرة الثلجية الساحرة، تأتي بكامل أناقتها لتسحر الأطفال بقصصها وأغانيها وقدراتها السحرية.",
        "image_url": "https://sspark.genspark.ai/cfimages?u1=A7sd2G21EWvzZaFxmUgIf4ys6ya8acJePUGV7YtUeHZM0ESeQyGs0Ga7kViWOsElvZNexqm8FGPkyIT0cSk93DnKGMJAd%2FVOQShoZ%2Fkz0kvBh9ab%2FhiDY3CqSVvwNyVFrf79oS864tf9iXHhu3me8A%3D%3D&u2=ml8ZiVXmY1NGX%2BIQ&width=2560",
        "category": "princess",
        "price_per_hour": 700,
        "color_theme": "#4ECDC4",
        "is_featured": True,
    },
    {
        "name_ar": "سبايدر مان",
        "name_en": "Spider-Man",
        "slug": "spiderman",
        "description": "البطل الخارق المحبوب! يأتي ليحمي الحفلة ويقدم عروض أكروباتية مذهلة للأطفال.",
        "image_url": "https://sspark.genspark.ai/cfimages?u1=rDUY1FyP8wGuBddAY39izXd2YUoBsfqk8BXoFF4B58nwcd%2FiM9aeSTaDdLM%2Fg%2Fh3aIgRkv%2BCB29GBnk%2BKeK8Q3BN%2BkTgVTmzJkAaC9MY0QbzZR69zVk5ZjWwoJLLpVuTzBxtvcY%2F&u2=JFGygGf9laLVDZZ0&width=2560",
        "category": "superhero",
        "price_per_hour": 700,
        "color_theme": "#FF6B6B",
        "is_featured": True,
    },
    {
        "name_ar": "ميكي ماوس",
        "name_en": "Mickey Mouse",
        "slug": "mickey-mouse",
        "description": "الفأر الأشهر في العالم بإطلالته الكلاسيكية المحبوبة، يجلب البهجة لكل عيد ميلاد.",
        "image_url": "https://sspark.genspark.ai/cfimages?u1=K2sKFog%2BpTSeJRa8kDxrWHxATftau4yypFqKLS5BVfjVjfeUlSGVZuIT9nxjnTcaTGu%2Bxg98n37T5XcVkPx46XKx2wxim1OtwyU7wMx1HTxrLmZq93AGvMEUsuy6mDGQ7MiY52E5kb4bYsmATQjk72Tfdz4Vaw%3D%3D&u2=%2FDL0a1cYC6GwWLk1&width=2560",
        "category": "cartoon",
        "price_per_hour": 600,
        "color_theme": "#A855F7",
        "is_featured": True,
    },
    {
        "name_ar": "ميني ماوس",
        "name_en": "Minnie Mouse",
        "slug": "minnie-mouse",
        "description": "صديقة ميكي اللطيفة بفستانها الأحمر المنقّط، شخصية مثالية لحفلات البنات.",
        "image_url": "https://sspark.genspark.ai/cfimages?u1=zfjX3rIoqTlV%2FkLfnFVC2PoNlgox6HmkSXtRNkH2JwAhUpu3SDpz3Gz6%2FBuhgb3mdmTSxaxEOlov578wqv6QaGDqlYUc0UceR1UsRIhqvrGZB5PwS4ZMJhiKdS01CKfpte%2FuwqJy1XCL&u2=EaIPp43ynRlRvIpP&width=2560",
        "category": "cartoon",
        "price_per_hour": 600,
        "color_theme": "#FF6B6B",
        "is_featured": False,
    },
    {
        "name_ar": "سونيك",
        "name_en": "Sonic",
        "slug": "sonic",
        "description": "القنفذ الأزرق السريع بسرعة الصوت، يجعل أطفالك يركضون ويلهون طوال الحفلة.",
        "image_url": "https://sspark.genspark.ai/cfimages?u1=AYxKnYYhJeI3Yy%2BvmHevSNQrMA%2BQbSIzSk0VdQGAlTK%2BI52HGYR2U45iWtJhnbyJ3dClDeqKlHPqooo80pjauSVEUllDh9VKUvHBxyifSC3XWEn7hvM%3D&u2=2TgMKLv2qGb4TZAm&width=2560",
        "category": "cartoon",
        "price_per_hour": 650,
        "color_theme": "#4ECDC4",
        "is_featured": True,
    },
    {
        "name_ar": "البهلوان المرح",
        "name_en": "Happy Clown",
        "slug": "clown",
        "description": "البهلوان الكلاسيكي بمهاراته في رسم الوجه ونفخ البالونات وعروضه الكوميدية الممتعة.",
        "image_url": "https://sspark.genspark.ai/cfimages?u1=JeyliaS4mjLAGFc5%2FPi2vfS6ikMjgnqVK5nz5wVp93I1s7%2FZ%2FVgp0ugGuxfLv4DKwM5rFmkR3OiILcLDxZBNq9yADICkv5inhKKrkCufPboJJXc7t5OIIyZy4nCsIsRrdFQanFwWSJRV3BozXd3Y7w%3D%3D&u2=shWDSyqRdmQBhkJj&width=2560",
        "category": "cartoon",
        "price_per_hour": 500,
        "color_theme": "#FFE66D",
        "is_featured": False,
    },
    {
        "name_ar": "بطل خارق",
        "name_en": "Superhero",
        "slug": "superhero",
        "description": "بطل خارق غامض يحمي الحفلة ويلهم الأطفال ليصبحوا أبطالاً أيضاً.",
        "image_url": "https://sspark.genspark.ai/cfimages?u1=c7V5zdgozgO7SU3eiA%2FW8BBxRMz8SOTCAhQdsZxZcqbc83qBQuF4Ep60oRQyqpKrQ00i9ZwfD523uzdwjq3Fnmvdyqzp6ohIE51gCCsnq4DVbMaWd2mLVXa194NknjMhFCQ2pTxpvj8J2InsyTHxmzlLHTL%2FQ36HrTjBK2UyrNJQ%2BPpgHz6QRNr75rXPD2Nq0jz2OtxVUC%2BWG3tzM1yqPq2%2FXqKVuqJHuWQYPQov9sdcne54mG936dU%3D&u2=gKBfc%2B0rC%2BYWIRBV&width=2560",
        "category": "superhero",
        "price_per_hour": 700,
        "color_theme": "#A855F7",
        "is_featured": False,
    },
]


SERVICES_DATA = [
    {
        "name_ar": "الباقة الأساسية",
        "name_en": "Basic Package",
        "slug": "basic",
        "description": "باقة مثالية لبداية احتفال مميز بميزانية معقولة. تتضمن شخصية واحدة وتزيين بسيط للمكان.",
        "short_desc": "احتفال بسيط وممتع بسعر مناسب",
        "price": 1500,
        "duration_hours": 2,
        "icon": "🎈",
        "image_url": "https://sspark.genspark.ai/cfimages?u1=Crv6rMSRL2IYIXC6EVxfL3z1UyEvjw3F3Ua2LlTLUnY%2BXyhpgbcURRqd4QtWYzPjIh9P%2B%2BPlurlz%2BOpnNnA5byol7FNB9irsjf%2Bt2c%2BOAPRqyRZBldXs9dH%2F2lKwYl7pV6f5mt7Sppx%2FRb%2BZ%2BfK9SRgNa7qDH6%2B3%2BFfs5keCuNMzKJ8wojY3lvdES4uVl%2Bt5ZWWzNxkhcIDDcIdj5v3N4uyuGxfXqtw4byyMEnjeyLtCANI9Rb0KCTBUUHLC47wIv4Hap9J3Y%2FUGrXDcTZNLQ99zbFz%2BXrk%2BcN4vdIQyTbcmiyedBA%3D%3D&u2=SSOwfUhRU0GIOV3w&width=2560",
        "features": [
            "شخصية ماسكوت واحدة لمدة ساعتين",
            "تزيين أساسي بالبالونات",
            "موسيقى خلفية",
            "ألعاب وأنشطة بسيطة",
            "حتى 15 طفل",
        ],
        "category": "birthday",
        "is_popular": False,
    },
    {
        "name_ar": "الباقة المتقدمة",
        "name_en": "Premium Package",
        "slug": "premium",
        "description": "الباقة الأكثر طلباً! تجربة احتفال متكاملة بشخصيتين وتزيين كامل للمكان مع تصوير احترافي.",
        "short_desc": "الأكثر طلباً - احتفال لا يُنسى",
        "price": 3500,
        "duration_hours": 3,
        "icon": "🎂",
        "image_url": "https://sspark.genspark.ai/cfimages?u1=jWh%2BVIlm68VTILEVytUZfE8BNcbnugXr7PBUjomDYhfEhCxdVhBYa0pm0uHDfk3Te%2BdENESx2RIvaLNelwcZcjc3A3SLcyruw9Y9JOUGcNW0buz5idM1g0bGF2XRYgwpyk6690BHDx7Gnp5mjKn5loB2sCg2ub711uNMWWeaE8TEYmOJmksXjamwc6U900UPMvdDuDWQ5b93G%2FExYo%2BFytUB4OF36AuVwZMM4PatT5cHYsa22LuGHkPUco1fcxq4KYCdL9F%2BN7ByLkbq%2FXpAGBBgfNk%3D&u2=40X4CH%2Bdr3dmlUwv&width=2560",
        "features": [
            "شخصيتان ماسكوت لمدة 3 ساعات",
            "تزيين شامل بالبالونات والثيم",
            "DJ ومؤثرات صوتية",
            "ألعاب وفقرات تفاعلية",
            "رسم على الوجه (Face Painting)",
            "تصوير فوتوغرافي احترافي",
            "حتى 30 طفل",
            "كيكة عيد ميلاد مزينة",
        ],
        "category": "birthday",
        "is_popular": True,
    },
    {
        "name_ar": "الباقة الذهبية VIP",
        "name_en": "VIP Gold Package",
        "slug": "vip",
        "description": "تجربة فاخرة لا مثيل لها! احتفال ملكي بكل التفاصيل لجعل يوم طفلك أسطورياً.",
        "short_desc": "تجربة ملكية فاخرة بكل التفاصيل",
        "price": 7500,
        "duration_hours": 4,
        "icon": "👑",
        "image_url": "https://sspark.genspark.ai/cfimages?u1=TJTTWHEOBH4SAHNQWi8%2FyY09YshZb1DeseNN9OHqKW97LBsVI%2BkcvMmrlceA85o6jA5LDHSGh2tzHLyJcdqKP9X2lQ%3D%3D&u2=ZELZNOHhOwa2RLNX&width=2560",
        "features": [
            "3-4 شخصيات ماسكوت لمدة 4 ساعات",
            "تزيين فاخر بثيم مخصص",
            "DJ احترافي مع نظام صوت متطور",
            "عروض أكروبات وسحر",
            "رسم على الوجه + تاتو مؤقت",
            "تصوير فيديو + فوتوغرافي 4K",
            "بوفيه ضيافة كامل",
            "حتى 60 طفل",
            "كيكة فاخرة + هدايا تذكارية",
            "آلة فقاقيع + ماكينة دخان",
        ],
        "category": "birthday",
        "is_popular": False,
    },
    {
        "name_ar": "حفلة سبوع كاملة",
        "name_en": "Sebou Celebration",
        "slug": "sebou",
        "description": "احتفال سبوع تقليدي مصري كامل بكل الطقوس والتفاصيل، تجربة عائلية لا تُنسى.",
        "short_desc": "سبوع تقليدي بكل الطقوس المصرية",
        "price": 2500,
        "duration_hours": 3,
        "icon": "👶",
        "image_url": "https://sspark.genspark.ai/cfimages?u1=GUxhJ6NN1eIJ%2FftoQVTijMz3XEWDRx3qrAMapW%2BpaPLrQbF5lvKo%2BkBfD%2Bpq2rXOo54M%2BYyZbrFyuggsjUXap8%2FyZmfZtH86JrI8Fk6eQqvVypFckgmP&u2=JddGjPOwceejcZ9j&width=2560",
        "features": [
            "تزيين شامل بثيم السبوع",
            "غربال + شموع تقليدية",
            "حلويات ومكسرات للضيوف",
            "موسيقى تراثية",
            "تصوير الذكريات",
            "هدايا تذكارية للحضور",
            "مدة 3 ساعات",
        ],
        "category": "sebou",
        "is_popular": False,
    },
    {
        "name_ar": "تأجير شخصية فقط",
        "name_en": "Mascot Only",
        "slug": "mascot-only",
        "description": "إذا كنت تريد إضافة شخصية ماسكوت فقط لحفلة موجودة بالفعل، هذه الخدمة المثالية لك.",
        "short_desc": "شخصية واحدة لمدة ساعة",
        "price": 600,
        "duration_hours": 1,
        "icon": "🎭",
        "image_url": "https://sspark.genspark.ai/cfimages?u1=pBfik%2B5eJs5Odv3I0ICOAIxmp%2BcwHT%2BG3hMrLmuF22VyOW4f4upIhkuqPeWHQm5qPD6ETHLhSNNs493KzieTX4ZkndyQ1182wMeYT5Oj4fN7gMUoVgXXxZBE0vjB6PK%2BffiYJkVpWvwbEOGLzKbmB3qwGCBg77WHa%2FTlbTYcCRTFE2s7vvdK02UDXRWLYE2VRtQoiYOhcytAHzL8Z3jSPlLa79hDfRUhpg8s%2FXZQzSGrClSc7USHZtYrxHtU9GrNqPVryJHm%2BtKm3ios45ge3BdYFNFgrOU9yg%3D%3D&u2=7lXKTS99VbO45Y%2BW&width=2560",
        "features": [
            "شخصية واحدة من اختيارك",
            "ساعة كاملة من المرح",
            "تفاعل مع الأطفال",
            "صور تذكارية",
            "إمكانية تمديد المدة",
        ],
        "category": "mascot",
        "is_popular": False,
    },
    {
        "name_ar": "تزيين فقط",
        "name_en": "Decoration Only",
        "slug": "decoration",
        "description": "خدمة التزيين الكامل للمكان دون شخصيات، مثالية لمن يفضل تنظيم النشاطات بنفسه.",
        "short_desc": "تزيين احترافي شامل",
        "price": 1200,
        "duration_hours": 0,
        "icon": "✨",
        "image_url": "https://sspark.genspark.ai/cfimages?u1=Lh2IOo7Jrt9Ne9ocMGPRB%2BoMjXGL539MAvTdkYbtUXFJA3qqwfcNfqN%2BVZZKhXHKue1pZQht32PlEJ8fsQIXsMnp615cQNKV15XY2fz%2BO274vg4LGsViwA%3D%3D&u2=vaPDpGWdwYITyMGU&width=2560",
        "features": [
            "تزيين كامل بثيم من اختيارك",
            "بالونات وأقواس",
            "خلفية فوتوغرافية",
            "طاولة الكيك المزينة",
            "إكسسوارات الحفلة",
        ],
        "category": "decoration",
        "is_popular": False,
    },
]


GALLERY_DATA = [
    # حفلات أعياد ميلاد
    {"image_url": "https://sspark.genspark.ai/cfimages?u1=jWh%2BVIlm68VTILEVytUZfE8BNcbnugXr7PBUjomDYhfEhCxdVhBYa0pm0uHDfk3Te%2BdENESx2RIvaLNelwcZcjc3A3SLcyruw9Y9JOUGcNW0buz5idM1g0bGF2XRYgwpyk6690BHDx7Gnp5mjKn5loB2sCg2ub711uNMWWeaE8TEYmOJmksXjamwc6U900UPMvdDuDWQ5b93G%2FExYo%2BFytUB4OF36AuVwZMM4PatT5cHYsa22LuGHkPUco1fcxq4KYCdL9F%2BN7ByLkbq%2FXpAGBBgfNk%3D&u2=40X4CH%2Bdr3dmlUwv&width=2560", "title": "حفلة عيد ميلاد ساحرة", "category": "birthday", "is_featured": True},
    {"image_url": "https://sspark.genspark.ai/cfimages?u1=Crv6rMSRL2IYIXC6EVxfL3z1UyEvjw3F3Ua2LlTLUnY%2BXyhpgbcURRqd4QtWYzPjIh9P%2B%2BPlurlz%2BOpnNnA5byol7FNB9irsjf%2Bt2c%2BOAPRqyRZBldXs9dH%2F2lKwYl7pV6f5mt7Sppx%2FRb%2BZ%2BfK9SRgNa7qDH6%2B3%2BFfs5keCuNMzKJ8wojY3lvdES4uVl%2Bt5ZWWzNxkhcIDDcIdj5v3N4uyuGxfXqtw4byyMEnjeyLtCANI9Rb0KCTBUUHLC47wIv4Hap9J3Y%2FUGrXDcTZNLQ99zbFz%2BXrk%2BcN4vdIQyTbcmiyedBA%3D%3D&u2=SSOwfUhRU0GIOV3w&width=2560", "title": "تزيين بالونات ملوّن", "category": "decoration", "is_featured": True},
    {"image_url": "https://sspark.genspark.ai/cfimages?u1=FLHNmnzU%2BPRH9c%2FivBFagZndtOVhVjd03c1bENWDu58qtdbh8YfCBeDzoi2c7eWdlW7QyW5Yhoz%2BOsQkjZ8C7GwKOjIUM833OSHp102YMFz5Oi66W%2FW4ZmJdvCyvKzj6Wmc5UgOfwp0agw7CAB9gsafASjgxi7RS8VbUBDbRtAKg9v33sXqW4McylfAplQ%3D%3D&u2=62L9uhVQzWjzIIL9&width=2560", "title": "احتفال مذهل بالحديقة", "category": "birthday", "is_featured": True},
    {"image_url": "https://sspark.genspark.ai/cfimages?u1=QGfBRjy9EfjgSC%2Fvd3%2BISY20ge5TfecVGgeHE78Hupbx5US2fWzujs1XyDDDtQdQHik6kc0r7IRk3IzzPqrTOhkEuN%2Fv6dOw1pFyXeutDpYripQGxQrnDReUHGK%2Fre9W%2Fng5tZchV0dKXWnzki%2Bo9fAZ1l8uJOzAouViCsHHciJU3qxMnHDuRQ%3D%3D&u2=JgUoJ0XhQRWUoSfT&width=2560", "title": "ضحكات وفرحة", "category": "birthday", "is_featured": False},
    {"image_url": "https://sspark.genspark.ai/cfimages?u1=9SZYr4leBOzsgU9Gglkh00Yxy3t%2BWhv5XSNHrpqAm2cO6Jl8cx9cjNhxGG%2BBIf%2FyMdJA3ikj%2FMLSWIMcEdvVDDq%2Bsw%3D%3D&u2=JZ8i8CMYDweVppeM&width=2560", "title": "بالونات باستيل أنيقة", "category": "decoration", "is_featured": False},
    {"image_url": "https://sspark.genspark.ai/cfimages?u1=jTJVouf%2F3nIyBes3qJyCcfCSuxR%2BbKOlLMHMPtr9htb24HaBKr3ADskFf3IHGi1acn01MT5E1ybdq0sjz31GF8L3tHQMvYKDLaHW4GtCQzvXilkmlJ6Dl44kpZHSZ7SK0Tz5BeG1WJPhPFrWNQ%3D%3D&u2=grsVoSZya5O5Y77J&width=2560", "title": "ماسكات في الحفل", "category": "mascot", "is_featured": True},
    {"image_url": "https://sspark.genspark.ai/cfimages?u1=8FXMFguRlBdc1Sn8v7GkKflUwymxf%2FwaQeUOnJ5WNV2WZSG7QQOFZiKN6wdjq61J60op3cIyH7KI6Z%2FfvWz2m%2FMD5BCHh6Y8%2FloWE6SiAt4Ksz3LK98bNBJtfmbXl76vhkjb6WvjkLNpi6aOTGt938eD35w6C%2BEaIaF9N3ibuRZdwGUmfmuxC%2FWEeBbcjTlMLCh09cZgj8JK950%3D&u2=uzstogZG6kkohrPA&width=2560", "title": "مجموعة شخصياتنا", "category": "mascot", "is_featured": True},
    {"image_url": "https://sspark.genspark.ai/cfimages?u1=NadkYtC6R%2BPJSyRexlu5g2bTslVbwMeqOQuk2rQas1Jn6ye%2FIgDRVGm5rhSkOv6qxfUUCW4E22u9Sn%2B6SzqWsb%2FneSKgzstr&u2=XVAdVfcCYFGlqJ9r&width=2560", "title": "شخصيات بأزياء كاملة", "category": "mascot", "is_featured": False},
    {"image_url": "https://sspark.genspark.ai/cfimages?u1=GUxhJ6NN1eIJ%2FftoQVTijMz3XEWDRx3qrAMapW%2BpaPLrQbF5lvKo%2BkBfD%2Bpq2rXOo54M%2BYyZbrFyuggsjUXap8%2FyZmfZtH86JrI8Fk6eQqvVypFckgmP&u2=JddGjPOwceejcZ9j&width=2560", "title": "احتفال السبوع التقليدي", "category": "sebou", "is_featured": True},
    {"image_url": "https://sspark.genspark.ai/cfimages?u1=4gW19rB543TTIWuvyCjNS2Z5aKIdlyqTptNp6BqQXSytuuMcrh9zzwsget5ZZUGvL7IgzLok5pfh6JG%2FwEpZBhfw5dFOfUbjKVjTpomXki71zBnXHcfcIFCbkGhDUEcRv60TVuQ%3D&u2=hZ9RLl1thAIJ%2FZOp&width=2560", "title": "تزيين سبوع راقي", "category": "sebou", "is_featured": False},
    {"image_url": "https://sspark.genspark.ai/cfimages?u1=UdgmAG6fijvp6oEhu7B2VSbhjoP3eMzN2QcnI1AwXRqj6Vp1saztlyEcnMCdIB69z7mHOW8Sij4q0s928yfykGWKXA%3D%3D&u2=f3IYullT1HUB7lPl&width=2560", "title": "ثيم مصري للسبوع", "category": "sebou", "is_featured": False},
    {"image_url": "https://sspark.genspark.ai/cfimages?u1=NoD%2BMR%2FwiSKF%2F5dPvU34gc9eMlxxLoxw292gCw%2BC%2B86qSt1RwfZC5inSmluFmEcMsBn8lo5Tkr6Mc6yfs7e%2F5Xn71aQXAtcx8lRrMSmGLmfUHoVTsKM3TPMho73COYKHfqGWiqtfYkUj&u2=QCgKJvmK8z2adzK%2F&width=2560", "title": "زينة سبوع مميزة", "category": "sebou", "is_featured": False},
    {"image_url": "https://sspark.genspark.ai/cfimages?u1=JeyliaS4mjLAGFc5%2FPi2vfS6ikMjgnqVK5nz5wVp93I1s7%2FZ%2FVgp0ugGuxfLv4DKwM5rFmkR3OiILcLDxZBNq9yADICkv5inhKKrkCufPboJJXc7t5OIIyZy4nCsIsRrdFQanFwWSJRV3BozXd3Y7w%3D%3D&u2=shWDSyqRdmQBhkJj&width=2560", "title": "رسم على الوجه", "category": "birthday", "is_featured": True},
    {"image_url": "https://sspark.genspark.ai/cfimages?u1=VZvBpJmVZeBYn4SNV3ZP0YQ6rTdFErtekGhTTznpmaKDgXFWw5%2B1V3xRLKzs0cy2Gv%2Bc6a2RUM3XlJ2hS%2FJ5HDotzPN02zniHd8lBPpM5lGr28LB5bVmxhdFRA%3D%3D&u2=q%2BI9X32fjWIfAGK3&width=2560", "title": "ترفيه ومرح", "category": "birthday", "is_featured": False},
    {"image_url": "https://sspark.genspark.ai/cfimages?u1=AcgLOr0en2WXiN1LEl%2B8mEhXLwAfzHUakCvoHbj%2B5Zq47Wt%2FY7XI9WMf2LrsTWEHdf44eB03g6STWPVIMTicLgKo2bFEQu%2FMf3Gn3FaQSaAOX4r9Pg7f1g%3D%3D&u2=yDHiPjrgEGDKp0qq&width=2560", "title": "كيكة وبالونات", "category": "decoration", "is_featured": False},
]


TESTIMONIALS_DATA = [
    {
        "customer_name": "سارة عبد الرحمن",
        "customer_role": "أم لطفلين",
        "rating": 5,
        "content": "تجربة لا تنسى! حفلة ابني كانت أسطورية. الشخصيات كانت احترافية والأطفال انبسطوا جداً. شكراً ليكم من قلبي ❤️",
        "event_type": "birthday",
        "avatar_url": "https://i.pravatar.cc/150?img=44",
    },
    {
        "customer_name": "أحمد المنصوري",
        "customer_role": "أب لثلاثة أطفال",
        "rating": 5,
        "content": "تنظيم رائع وفريق محترف. سبونج بوب وميكي ماوس كانوا مثاليين والتزيين كان فوق التوقعات. أنصح بهم بشدة!",
        "event_type": "birthday",
        "avatar_url": "https://i.pravatar.cc/150?img=12",
    },
    {
        "customer_name": "ندى حسن",
        "customer_role": "أم حديثة",
        "rating": 5,
        "content": "سبوع بنتي كان مثالي. كل التفاصيل كانت مدروسة والثيم المصري التقليدي كان جميل جداً. كل العائلة استمتعت!",
        "event_type": "sebou",
        "avatar_url": "https://i.pravatar.cc/150?img=47",
    },
    {
        "customer_name": "محمد كمال",
        "customer_role": "أب",
        "rating": 5,
        "content": "إلسا كانت مدهشة! بنتي لسه بتتكلم عن الحفلة لحد دلوقتي. الباقة الذهبية تستاهل كل قرش. شكراً جزيلاً لفريق العمل المحترف.",
        "event_type": "birthday",
        "avatar_url": "https://i.pravatar.cc/150?img=33",
    },
    {
        "customer_name": "ريم السيد",
        "customer_role": "منظمة فعاليات",
        "rating": 5,
        "content": "تعاملت معاهم كذا مرة لحفلات شركتي والأهل. دائماً مستوى عالي والتزام بالمواعيد. فريق محترف جداً وإبداع في التفاصيل.",
        "event_type": "birthday",
        "avatar_url": "https://i.pravatar.cc/150?img=49",
    },
    {
        "customer_name": "كريم صلاح",
        "customer_role": "أب لطفلة",
        "rating": 5,
        "content": "سبايدر مان كان البطل الحقيقي للحفلة! الأطفال طاروا من الفرحة. التصوير كان احترافي والذكريات راح تفضل معانا للأبد.",
        "event_type": "birthday",
        "avatar_url": "https://i.pravatar.cc/150?img=15",
    },
]


def seed_database():
    """ملء قاعدة البيانات بالبيانات الأولية"""
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        # تجنب التكرار - فقط اضف لو فاضي
        if db.query(models.Character).count() == 0:
            print("📦 جاري إضافة الشخصيات...")
            for c in CHARACTERS_DATA:
                db.add(models.Character(**c))
            db.commit()
            print(f"✅ تمت إضافة {len(CHARACTERS_DATA)} شخصية")

        if db.query(models.Service).count() == 0:
            print("📦 جاري إضافة الخدمات...")
            for s in SERVICES_DATA:
                db.add(models.Service(**s))
            db.commit()
            print(f"✅ تمت إضافة {len(SERVICES_DATA)} خدمة")

        if db.query(models.GalleryItem).count() == 0:
            print("📦 جاري إضافة المعرض...")
            for g in GALLERY_DATA:
                db.add(models.GalleryItem(**g))
            db.commit()
            print(f"✅ تمت إضافة {len(GALLERY_DATA)} صورة في المعرض")

        if db.query(models.Testimonial).count() == 0:
            print("📦 جاري إضافة شهادات العملاء...")
            for t in TESTIMONIALS_DATA:
                db.add(models.Testimonial(**t))
            db.commit()
            print(f"✅ تمت إضافة {len(TESTIMONIALS_DATA)} شهادة")

        # إضافة مستخدم أدمن افتراضي
        if db.query(models.User).filter(models.User.username == "admin").first() is None:
            print("👤 جاري إضافة المستخدم الأدمن...")
            admin = models.User(
                username="admin",
                email="admin@partymagic.eg",
                hashed_password=hash_password("admin123"),
                full_name="مدير النظام",
                is_admin=True,
            )
            db.add(admin)
            db.commit()
            print("✅ تم إنشاء حساب الأدمن (admin / admin123)")

        print("🎉 اكتملت تهيئة قاعدة البيانات!")
    except Exception as e:
        print(f"❌ خطأ في تهيئة قاعدة البيانات: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
