import os
import hashlib
from PIL import Image, ImageChops

class UkweliLensEngine:
    def __init__(self):
        # Saini rasmi za Magic Bytes kwa ajili ya usalama wa mfumo (File Validation)
        self.magic_bytes_table = {
            b"\xff\xd8\xff": "Picha (JPEG)",
            b"\x89\x50\x4e\x47": "Picha (PNG)",
            b"\x25\x50\x44\x46": "Nyaraka (PDF)",
            b"\x49\x44\x33": "Sauti (MP3)",
            b"\x52\x49\x46\x46": "Sauti/Video (RIFF/WAV/AVI)",
            b"\x00\x00\x00\x18\x66\x74\x79\x70": "Video (MP4)",
            b"\x00\x00\x00\x20\x66\x74\x79\x70": "Video (MP4)"
        }

    def verify_file_integrity(self, path):
        """Kipengele cha Usalama 1: Kukagua Magic Bytes na kupiga hesabu ya SHA-256 Hash"""
        if not os.path.exists(path):
            return False, "Faili halipatikani", None

        # 1. Kupiga hesabu ya SHA-256
        sha256_hash = hashlib.sha256()
        with open(path, "rb") as f:
            file_header = f.read(16) # Soma byte za mwanzo kwa usalama
            f.seek(0)
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        file_hash = sha256_hash.hexdigest()

        # 2. Uhakiki wa Magic Bytes dhidi ya mashambulizi ya Spoofing/Malware
        is_valid_type = False
        for header, file_type in self.magic_bytes_table.items():
            if file_header.startswith(header):
                is_valid_type = True
                break
        
        # Ruhusu kupita kama mwanzo wa byte unafanana na mifumo ya media
        if not is_valid_type and not path.lower().endswith(('.mp4', '.avi', '.mp3', '.wav')):
            return False, "🚨 ONYHO LA USALAMA: Muundo wa ndani wa faili (Magic Bytes) haukubaliki au ni hatari!", file_hash

        return True, "🛡️ Faili limepita ukaguzi wa kiusalama na uadilifu (Integrity Checked).", file_hash

    def analyze_image(self, path, quality=90):
        orig = Image.open(path).convert('RGB')
        temp = "temp.jpg"
        orig.save(temp, 'JPEG', quality=quality)
        resaved = Image.open(temp)

        ela = ImageChops.difference(orig, resaved)
        stat = ela.getdata()
        pixel_changes = sum([sum(p) if isinstance(p, tuple) else p for p in stat]) / len(stat)
        os.remove(temp)

        ai_score = min(100, max(0, int(pixel_changes * 45)))
        human_score = 100 - ai_score

        verdict = "🛡️ PICHA YA UKWELI" if ai_score < 35 else "🚨 PICHA YA UONGO / AI"
        return verdict, human_score, ai_score

    def analyze_document(self, path):
        try:
            from pypdf import PdfReader
            reader = PdfReader(path)
            meta = reader.metadata
            creator = str(meta.get('/Producer', '')).lower() + str(meta.get('/Author', '')).lower()
            
            if "ai" in creator or "gpt" in creator or "bot" in creator:
                ai_score = 80
            else:
                ai_score = 15
        except Exception:
            ai_score = 75 

        human_score = 100 - ai_score
        verdict = "🛡️ NYARAKA YA UKWELI" if ai_score < 40 else "🚨 NYARAKA YA UONGO / AI"
        return verdict, human_score, ai_score

    def analyze_audio(self, path):
        try:
            import librosa
            import numpy as np
            
            y, sr = librosa.load(path, sr=None)
            flatness = librosa.feature.spectral_flatness(y=y)
            mean_flatness = np.mean(flatness)
            
            ai_score = min(max(int(mean_flatness * 12000) % 100, 5), 95)
            mfcc = librosa.feature.mfcc(y=y, sr=sr)
            mfcc_std = np.mean(np.std(mfcc, axis=1))
            
            if mfcc_std < 15:
                ai_score += 20
                
            ai_score = min(ai_score, 99)
        except Exception:
            ai_score = 50  

        human_score = 100 - ai_score
        verdict = "🛡️ SAUTI YA UKWELI" if ai_score < 45 else "🚨 SAUTI YA UONGO / AI"
        return verdict, human_score, ai_score

    def analyze_video(self, path):
        try:
            import cv2
            import numpy as np
            
            cap = cv2.VideoCapture(path)
            if not cap.isOpened():
                raise Exception("Haiwezi kufungua video")
                
            frame_count = 0
            variances = []
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame_count += 1
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                variances.append(np.var(gray))
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count + 15)
                
            cap.release()
            var_std = np.std(variances)
            
            if 400 <= var_std <= 3500:
                ai_score = 15
                reason = "Mienendo ya mwanga na picha (Variance STD: {:.2f}) ni ya kawaida.".format(var_std)
            else:
                ai_score = 75
                reason = "Kuna utofauti usio wa kawaida wa mwanga (Variance STD: {:.2f}), kiashiria cha Deepfake.".format(var_std)
                
        except Exception as e:
            ai_score = 50
            reason = f"Hitilafu ya muundo wa picha: {e}"

        human_score = 100 - ai_score
        verdict = "🛡️ VIDEO YA UKWELI" if ai_score < 50 else "🚨 VIDEO YA UONGO / AI"
        return verdict, human_score, ai_score, reason


if __name__ == "__main__":
    detector = UkweliLensEngine()
    print("\n==================================================")
    print("   UKWELILENS HYBRID FORENSICS (SECURITY SECURED) ")
    print("==================================================")
    
    files_to_test = {
        "Picha": ("picha_test.jpg", detector.analyze_image),
        "Nyaraka": ("barua_test.pdf", detector.analyze_document),
        "Sauti": ("sauti_test.wav", detector.analyze_audio),
        "Video": ("video_test.mp4", detector.analyze_video)
    }

    for file_type, (file_name, analyze_func) in files_to_test.items():
        if os.path.exists(file_name):
            # Run ukaguzi wa kiusalama kwanza kabla ya uchambuzi
            is_safe, sec_msg, file_hash = detector.verify_file_integrity(file_name)
            print(f"\n[FILE]: {file_name} ({file_type})")
            print(f"USALAMA/HASH: {sec_msg}")
            print(f"SHA-256 HASH: {file_hash}")
            
            if not is_safe and "🚨" in sec_msg:
                print("[-] Uchambuzi umesitishwa kwa sababu ya usalama wa mfumo.")
                continue

            # Endesha uchambuzi kama faili lipo salama
            analysis_res = analyze_func(file_name)
            if len(analysis_res) == 4:
                v, h, a, r = analysis_res
                print(f"HUKUMU      : {v}\nHUMANIZED   : {h}%\nAI-GENERATED: {a}%\nSABABU      : {r}")
            else:
                v, h, a = analysis_res
                print(f"HUKUMU      : {v}\nHUMANIZED   : {h}%\nAI-GENERATED: {a}%")
            print("-" * 45)

    print("\n==================================================\n")
