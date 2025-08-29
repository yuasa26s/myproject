#!/usr/bin/env python3
import pandas as pd
import os
from datetime import datetime

class LotteryVerifier:
    def __init__(self, base_path="/home/{}/lottery_project".format(os.getenv('USER'))):
        self.base_path = base_path
        self.data_path = os.path.join(base_path, "data")
        self.output_path = os.path.join(base_path, "output")
        
        # ディレクトリ作成
        os.makedirs(self.data_path, exist_ok=True)
        os.makedirs(self.output_path, exist_ok=True)
    
    def verify_results(self, members_file="member_data.xlsx", results_file="lottery_results.xlsx"):
        try:
            # データ読み込み
            members_path = os.path.join(self.data_path, members_file)
            results_path = os.path.join(self.data_path, results_file)
            
            members = pd.read_excel(members_path)
            results = pd.read_excel(results_path)
            
            # 基本統計
            member_count = len(members)
            winner_count = len(results)
            win_rate = winner_count / member_count * 100
            
            print("=== 抽選結果確認 ===")
            print(f"全会員数: {member_count}")
            print(f"当選者数: {winner_count}")
            print(f"当選率: {win_rate:.2f}%")
            
            # 重複チェック
            duplicates = results[results.duplicated(['member_id'], keep=False)]
            if len(duplicates) > 0:
                print(f"⚠️ 重複当選者: {len(duplicates)}名")
            else:
                print("✅ 重複当選者なし")
            
            # レポート保存
            self.save_report(member_count, winner_count, win_rate, len(duplicates))
            
        except Exception as e:
            print(f"エラー: {e}")
    
    def save_report(self, member_count, winner_count, win_rate, duplicate_count):
        report_file = os.path.join(self.output_path, f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("抽選結果分析レポート\n")
            f.write(f"生成日時: {datetime.now()}\n")
            f.write("==========================\n")
            f.write(f"全会員数: {member_count}\n")
            f.write(f"当選者数: {winner_count}\n")
            f.write(f"当選率: {win_rate:.2f}%\n")
            f.write(f"重複当選者: {duplicate_count}名\n")
        
        print(f"レポートを保存しました: {report_file}")

if __name__ == "__main__":
    verifier = LotteryVerifier()
    verifier.verify_results()