from flask import Flask, send_from_directory, request, jsonify, render_template
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Agg')  
import matplotlib.animation as animation
import os
import threading 
import tkinter as tk
from PIL import Image, ImageTk
import time
import webbrowser

# تأكد من وجود مجلد "static"
if not os.path.exists("static"):
    os.makedirs("static")

app = Flask(__name__)

# بيانات الأسبرين
aspirin_data = {
    "histoire": {
        "description": "📜 تم تصنيع الأسبرين في عام 1897 من قبل 🧑‍🔬 فيليكس هوفمان في شركة باير. قبل ذلك، كان يتم استخدام 🌿 الساليسين، المستخرج من شجرة الصفصاف، منذ العصور القديمة لعلاج الألم والحمى.",
        "dates_importantes": [
            "🏺 العصور القديمة: استخدام لحاء الصفصاف لعلاج الألم والحمى.",
            "🧪 1828: يوهان بوشنر يعزل الساليسين.",
            "⚗️ 1853: تشارلز فريدريك جيرهارد يقوم بأول تصنيع لحمض الأسيتيل ساليسيليك.",
            "💊 1897: فيليكس هوفمان يصنع الأسبرين الحديث في شركة باير."
        ]
    },
    "decouverte": {
        "description": "🔬 يعود الاستخدام الطبي لحاء الصفصاف إلى العصور القديمة. في عام 1828، عزل يوهان بوشنر الساليسين، وفي عام 1897، قام فيليكس هوفمان بتصنيع حمض الأسيتيل ساليسيليك، مما أدى إلى إنشاء الأسبرين الحديث.",
        "personnages_cles": [
            "🌿 أبقراط: كان يستخدم لحاء الصفصاف لتخفيف الألم.",
            "🧪 يوهان بوشنر: قام بعزل الساليسين في عام 1828.",
            "⚗️ تشارلز فريدريك جيرهارد: قام بأول تصنيع لحمض الأسيتيل ساليسيليك في عام 1853.",
            "💊 فيليكس هوفمان: قام بتصنيع الأسبرين في عام 1897."
        ]
    },
    "preparation": {
        "reactifs": ["🧪 حمض الساليسيليك", "⚗️ أنهيدريد الأسيتيك", "🛠️ حمض الكبريتيك (عامل مساعد)"],
        "reaction": "⚗️ حمض الساليسيليك + أنهيدريد الأسيتيك → 💊 حمض الأسيتيل ساليسيليك (أسبرين) + 🧴 حمض الأسيتيك",
        "etapes": [
            "1️⃣ اخلط حمض الساليسيليك مع أنهيدريد الأسيتيك.",
            "2️⃣ أضف بضع قطرات من حمض الكبريتيك.",
            "3️⃣ سخن الخليط إلى 🔥 50-60°C لمدة 15 دقيقة.",
            "4️⃣ برد الخليط وأضف الماء البارد لترسيب الأسبرين.",
            "5️⃣ قم بترشيح البلورات وجففها."
        ]
    },
    "synthese_chimique": {
        "reactifs": ["🧪 حمض الساليسيليك", "⚗️ أنهيدريد الأسيتيك", "🛠️ حمض الكبريتيك (عامل مساعد)"],
        "reactions": "C7H6O3 + C4H6O3 → C9H8O4 + C2H4O2",
        "reaction": "⚗️ حمض الساليسيليك + أنهيدريد الأسيتيك → 💊 حمض الأسيتيل ساليسيليك (أسبرين) + 🧴 حمض الأسيتيك",
        "etapes": [
            "1️⃣ اخلط حمض الساليسيليك مع أنهيدريد الأسيتيك.",
            "2️⃣ أضف بضع قطرات من حمض الكبريتيك.",
            "3️⃣ سخن الخليط إلى 🔥 50-60°C لمدة 15 دقيقة.",
            "4️⃣ برد الخليط وأضف الماء البارد لترسيب الأسبرين.",
            "5️⃣ قم بترشيح البلورات وجففها."
        ]
    },
    "utilisations_anciennes": [
        "🏺 العصور القديمة: شاي لحاء الصفصاف لعلاج 🌡️ الحمى و 🤕 الألم.",
        "📜 400 ق.م: 🏛️ أبقراط يستخدمه لعلاج آلام المفاصل.",
        "⏳ العصور الوسطى: كان يستخدمه المعالجون والأعشابيون.",
        "🧪 القرن الثامن عشر: إدوارد ستون يكتشف آثاره ويقارنه بالكينين."
    ],
    "utilisations_modernes": [
        "💊 مسكن للألم: يعالج الصداع وآلام العضلات.",
        "🔥 مضاد للالتهابات: علاج الروماتيزم والتهاب المفاصل.",
        "🌡️ خافض للحرارة: يقلل الحمى.",
        "❤️ مضاد للتخثر: الوقاية من السكتات الدماغية والنوبات القلبية."
    ],
    "effets_secondaires": [
        "⚠️ تهيج المعدة وقرحة المعدة.",
        "🩸 اضطرابات النزيف (تسييل الدم).",
        "🤧 ردود فعل تحسسية محتملة.",
        "🚫 لا تأخذه في حالة حساسية من الأسبرين أو اضطرابات تخثر الدم."
    ],
    "generalites": {
        "description": "💊 الأسبرين، أو حمض الأسيتيل ساليسيليك، هو دواء مضاد للالتهابات غير ستيرويدي (AINS) 🦠 يساعد في تخفيف الألم 😖، خفض الحمى 🌡️، وتقليل الالتهاب 🔥. المادة الفعالة تمنع الإنزيمات التي تنتج مواد كيميائية تسمى البروستاجلاندين، المسؤولة عن الألم والالتهاب 🤕.",
        "proprietes": [
            "مسكن للألم (مسكن)",
            "مضاد للالتهابات",
            "خافض للحرارة (يقلل الحمى)",
            "مضاد للتخثر (يسيل الدم)"
        ]
    }
}

def get_aspirin_info(topic):
    return aspirin_data.get(topic, "لا أستطيع العثور على هذه المعلومات حول الأسبرين.")

def draw_schema():
    try:
        # إنشاء مخطط باستخدام matplotlib
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 5)
        ax.axis("off")
        
        ax.text(1, 2.5, "حمض الساليسيليك", fontsize=12, ha='center', va='center', bbox=dict(facecolor='lightblue', edgecolor='black'))
        ax.text(5, 2.5, "+ أنهيدريد الأسيتيك", fontsize=12, ha='center', va='center', bbox=dict(facecolor='lightgreen', edgecolor='black'))
        ax.text(9, 2.5, "= أسبرين", fontsize=12, ha='center', va='center', bbox=dict(facecolor='lightcoral', edgecolor='black'))
        
        ax.arrow(2, 2.5, 2, 0, head_width=0.2, head_length=0.3, fc='black', ec='black')
        ax.arrow(6, 2.5, 2, 0, head_width=0.2, head_length=0.3, fc='black', ec='black')
        
        plt.title("مخطط تصنيع الأسبرين")
        
        plt.savefig("static/schema.png")
        plt.close()
        print("تم إنشاء المخطط وحفظه بنجاح.")
    except Exception as e:
        print(f"حدث خطأ أثناء إنشاء المخطط: {e}")

def show_schema_tkinter():
    threading.Thread(target=open_tkinter_window, daemon=True).start()

def open_tkinter_window():
    root = tk.Tk()
    root.title("مخطط تصنيع الأسبرين")

    image = Image.open("static/schema.png")
    image = image.resize((600, 400))
    photo = ImageTk.PhotoImage(image)

    label = tk.Label(root, image=photo)
    label.image = photo
    label.pack()

    close_btn = tk.Button(root, text="إغلاق", command=root.destroy)
    close_btn.pack()

    root.mainloop()

def chatbot(question):
    question = question.lower().strip()  

    if any(word in question for word in ["شكرا", "شكرا جزيلا", "thanks", "thank you"]):
        return "🤖 على الرحب والسعة! لا تتردد في طرح المزيد من الأسئلة إذا كنت بحاجة إلى مساعدة. 😊"

    elif any(word in question for word in ["من أنت", "تعريف", "من تكون", "عرف نفسك", "ماذا تفعل", "كيف تعمل", "شات بوت", "من قام بإنشائك", "مبرمج", "أنس قادة", "أنس", "قادة", "مشروع", "20/20", "مرحبا"]):
        info = "🤖 مرحبا! أنا Ask_Asperine، بوت ذكاء اصطناعي غير توليدي (بوت) تم إنشاؤه بواسطة أنس قادة باستخدام بايثون لمشروعه التكنولوجي. أنا متخصص في تقديم معلومات عن الأسبرين. اطرح علي سؤالا، وسأبذل قصارى جهدي للإجابة عليه! 😊"
        return info
    
    elif any(word in question for word in ["آثار جانبية", "ما هي آثاره الجانبية", "مخاطر", "خطر", "خطير", "حساسية", "موانع الاستخدام", "نزيف", "مخاطرة", "نزيف", "معدة", "موانع", "قرحة", "أعراض", "مضاعفات", "ممنوع", "طفل", "مشكلة", "صحة", "عرض"]):
        info2 = get_aspirin_info("effets_secondaires")
        return "\n".join(info2)
    
    elif any(word in question for word in ["اكتشاف", "اكتشافات", "من اكتشفه", "اكتشف", "أصل", "أصول", "العصور الوسطى"]):
        info = get_aspirin_info("decouverte")
        return info["description"]
    
    elif any(word in question for word in ["تاريخ", "من قام بإنشائه", "أصل", "متى", "من اخترعه", "من اكتشفه"]):
        info = get_aspirin_info("histoire")
        return info["description"]
    
    elif any(word in question for word in ["قديم", "قديمة", "العصور القديمة", "تقليدي", "تاريخ الاستخدام", "طبيعي", "قبل"]):
        info = get_aspirin_info("utilisations_anciennes")
        return "\n".join(info)
    
    elif any(word in question for word in ["استخدامات حديثة", "استخدامات", "إيجابيات", "اليوم", "حالي", "مسكن", "مضاد للالتهابات", "حمى", "مضاد للتخثر", "سكتة دماغية", "نوبة قلبية", "التهاب المفاصل", "طب القلب"]):
        info = get_aspirin_info("utilisations_modernes")
        return "\n".join(info)
    
    elif any(word in question for word in ["تحضير", "تصنيع", "تصنيع كيميائي", "تفاعل كيميائي", "مواد تفاعل", "صيغة"]):
        info = get_aspirin_info("preparation")
        return f"المواد التفاعلية: {', '.join(info['reactifs'])}\nالتفاعل: {info['reaction']}\nالخطوات:\n" + "\n".join(info["etapes"])
    
    elif any(word in question for word in ["كيميائي", "تصنيع كيميائي", "مصنع", "منتج"]):
        info = get_aspirin_info("synthese_chimique")
        return f"المواد التفاعلية: {', '.join(info['reactifs'])}\nالتفاعلات: {info['reactions']}\nالخطوات:\n" + "\n".join(info["etapes"])
    
    elif any(word in question for word in ["تعريف الأسبرين", "ما هو الأسبرين", "ما هو الأسبرين", "اشرح الأسبرين", "كيف يعمل الأسبرين"]):
        info = get_aspirin_info("generalites")
        return info["description"]
    
    else:
        return "أنا لست متأكدا من فهم سؤالك. حاول طرح سؤال آخر! أو تحقق من الإملاء!"

@app.route("/")
def home():
    return render_template("index1.html", message="مرحبا، أهلا بك  تم إنشاؤه بواسطة أنس قادة لمشروعه التكنولوجي. (من فضلك إذا كنت الأستاذة، أعطني 20/20 😆)", time=int(time.time()))

@app.route("/chatbot", methods=["POST"])
def chatbot_api():
    question = request.form.get("question")
    if not question:
        return jsonify({"error": "يرجى طرح سؤال"})
    
    response = chatbot(question)
    if isinstance(response, (list, dict)):
        response = "\n".join(response) if isinstance(response, list) else str(response)
    return jsonify({"response": response})

@app.route("/static/audio/<filename>")
def get_audio(filename):
    return send_from_directory("static/audio", filename, as_attachment=False)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
url = "http://127.0.0.1:5000"
webbrowser.open(url)

if __name__ == "__main__":
    app.run(debug=True)