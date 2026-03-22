import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, scrolledtext, ttk

_REPO = Path(__file__).resolve().parent.parent
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))


def _open_results_window(parent, data):
    win = tk.Toplevel(parent)
    win.title("Langlaw — 분석 결과")
    win.minsize(640, 480)
    win.geometry("800x620")

    nb = ttk.Notebook(win)
    nb.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    def add_tab(title, body: str):
        frame = ttk.Frame(nb)
        nb.add(frame, text=title)
        kw = {"wrap": tk.WORD}
        if _darwin_font():
            kw["font"] = ("SF Pro Text", 12)
        text = scrolledtext.ScrolledText(frame, **kw)
        text.pack(fill=tk.BOTH, expand=True)
        text.insert(tk.END, body)
        text.configure(state=tk.DISABLED)

    kw_lines = "\n".join(data["keywords"]) if data["keywords"] else "(키워드 없음)"
    add_tab("키워드", kw_lines)

    cases_lines = "\n\n".join(
        f"{c['사건명']}\n{c['사건번호']} · {c['선고일자']} · {c['법원명']}\n{c['판례상세링크']}"
        for c in data["cases"]
    ) if data["cases"] else "(검색된 판례 없음)"
    add_tab("판례", cases_lines)

    laws_lines = "\n\n".join(
        f"{l.get('조문번호', '')} {l.get('제목', '')}\n{l.get('내용', '')[:500]}"
        for l in data["laws"]
    ) if data["laws"] else "(매칭 법령 없음)"
    add_tab("법령", laws_lines)

    add_tab("판단 요약", data["judgment"] or "(내용 없음)")


def _darwin_font():
    import sys
    return sys.platform == "darwin"


def main():
    root = tk.Tk()
    root.title("Langlaw")
    root.minsize(520, 360)
    root.geometry("640x420")

    frm = ttk.Frame(root, padding=12)
    frm.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frm, text="사건 설명").pack(anchor=tk.W)
    ib_kw = {"height": 12, "wrap": tk.WORD}
    if _darwin_font():
        ib_kw["font"] = ("SF Pro Text", 13)
    input_box = scrolledtext.ScrolledText(frm, **ib_kw)
    input_box.pack(fill=tk.BOTH, expand=True, pady=(4, 8))

    status = ttk.Label(frm, text="준비됨")
    status.pack(anchor=tk.W)

    btn_row = ttk.Frame(frm)
    btn_row.pack(fill=tk.X, pady=(8, 0))

    def run_analysis():
        from src.legal_reasoner import analyze_case

        case_text = input_box.get("1.0", tk.END).strip()
        if not case_text:
            messagebox.showwarning("Langlaw", "사건 설명을 입력해 주세요.")
            return

        run_btn.configure(state=tk.DISABLED)
        status.configure(text="분석 중… (API 호출에 시간이 걸릴 수 있습니다)")

        def work():
            try:
                data = analyze_case(case_text)
                root.after(0, lambda: _finish_ok(data))
            except Exception as e:
                root.after(0, lambda err=e: _finish_err(err))

        def _finish_ok(data):
            run_btn.configure(state=tk.NORMAL)
            status.configure(text="완료 — 결과 창을 확인하세요.")
            _open_results_window(root, data)

        def _finish_err(err):
            run_btn.configure(state=tk.NORMAL)
            status.configure(text="오류가 발생했습니다.")
            messagebox.showerror("Langlaw", str(err))

        threading.Thread(target=work, daemon=True).start()

    run_btn = ttk.Button(btn_row, text="분석 실행", command=run_analysis)
    run_btn.pack(side=tk.LEFT)

    ttk.Button(btn_row, text="종료", command=root.destroy).pack(side=tk.RIGHT)

    root.mainloop()


if __name__ == "__main__":
    main()
