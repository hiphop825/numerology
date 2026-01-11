import datetime
from typing import Dict, List, Tuple


class BaziCalculator:
    """
    八字排盤系統
    根據出生日期時間計算八字（年柱、月柱、日柱、時柱）
    """
    
    # 天干
    HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    
    # 地支
    EARTHLY_BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 月份地支
    MONTH_BRANCHES = ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑']
    
    # 二十四節氣對照表 (節氣名稱，天數累計)
    SOLAR_TERMS = [
        ('小寒', 5), ('大寒', 20), ('立春', 4), ('雨水', 19), ('驚蟄', 6), ('春分', 21),
        ('清明', 5), ('穀雨', 21), ('立夏', 7), ('小滿', 22), ('芒種', 8), ('夏至', 23),
        ('小暑', 7), ('大暑', 23), ('立秋', 8), ('處暑', 23), ('白露', 8), ('秋分', 23),
        ('寒露', 8), ('霜降', 23), ('立冬', 8), ('小雪', 22), ('大雪', 7), ('冬至', 22)
    ]
    
    def __init__(self):
        pass
    
    def get_heavenly_stem(self, index: int) -> str:
        """獲取天干"""
        return self.HEAVENLY_STEMS[index % 10]
    
    def get_earthly_branch(self, index: int) -> str:
        """獲取地支"""
        return self.EARTHLY_BRANCHES[index % 12]
    
    def get_year_stem_branch(self, year: int) -> str:
        """計算年柱干支"""
        # 年干：(年份 - 4) % 10
        stem_index = (year - 4) % 10
        # 年支：(年份 - 4) % 12
        branch_index = (year - 4) % 12
        
        return self.get_heavenly_stem(stem_index) + self.get_earthly_branch(branch_index)
    
    def get_month_stem_branch(self, year: int, month: int, day: int) -> str:
        """計算月柱干支 (使用節氣計算)"""
        # 簡化計算：根據月份決定地支，天干則根據年干推算
        month_branch = self.MONTH_BRANCHES[(month - 2 + 12) % 12]  # 月支
        
        # 計算月干：根據年干和月份推算
        year_stem_index = (year - 4) % 10
        # 月干公式：年干數×2 + 月份數 (正月為寅月)
        month_stem_index = (year_stem_index * 2 + month - 1) % 10
        
        return self.get_heavenly_stem(month_stem_index) + month_branch
    
    def get_day_stem_branch(self, year: int, month: int, day: int) -> str:
        """計算日柱干支 (簡化算法)"""
        # 使用蔡勒公式計算星期幾的變形來計算干支
        # 簡化處理：基於某個已知日期的干支來推算
        base_date = datetime.date(2024, 1, 1)  # 假設此日為甲辰日
        target_date = datetime.date(year, month, day)
        
        days_diff = (target_date - base_date).days
        
        # 甲辰日的干支索引 (甲為0，辰為4)
        base_stem_idx = 0  # 甲
        base_branch_idx = 4  # 辰
        
        day_stem_idx = (base_stem_idx + days_diff) % 10
        day_branch_idx = (base_branch_idx + days_diff) % 12
        
        return self.get_heavenly_stem(day_stem_idx) + self.get_earthly_branch(day_branch_idx)
    
    def get_hour_stem_branch(self, day_stem: str, hour: int) -> str:
        """計算時柱干支"""
        # 時支：根據小時計算 (24小時制轉換為子時開始的12個時辰)
        hour_branch_idx = (hour + 1) // 2 % 12  # 子時為23-1點，所以要加1
        hour_branch = self.get_earthly_branch(hour_branch_idx)
        
        # 時干：根據日干和時支計算
        day_stem_idx = self.HEAVENLY_STEMS.index(day_stem[0])
        # 時干公式：日干數×2 + 時支數 - 2 (如果結果>10則減10)
        hour_stem_idx = (day_stem_idx * 2 + hour_branch_idx - 2) % 10
        hour_stem = self.get_heavenly_stem(hour_stem_idx)
        
        return hour_stem + hour_branch
    
    def calculate_bazi(self, birth_datetime: datetime.datetime) -> Dict[str, str]:
        """計算完整八字"""
        year = birth_datetime.year
        month = birth_datetime.month
        day = birth_datetime.day
        hour = birth_datetime.hour
        
        year_stem_branch = self.get_year_stem_branch(year)
        month_stem_branch = self.get_month_stem_branch(year, month, day)
        day_stem_branch = self.get_day_stem_branch(year, month, day)
        hour_stem_branch = self.get_hour_stem_branch(day_stem_branch, hour)
        
        return {
            'year': year_stem_branch,
            'month': month_stem_branch,
            'day': day_stem_branch,
            'hour': hour_stem_branch
        }
    
    def get_zodiac_sign(self, earthly_branch: str) -> str:
        """獲取生肖"""
        zodiac_map = {
            '子': '鼠', '丑': '牛', '寅': '虎', '卯': '兔',
            '辰': '龍', '巳': '蛇', '午': '馬', '未': '羊',
            '申': '猴', '酉': '雞', '戌': '狗', '亥': '豬'
        }
        return zodiac_map.get(earthly_branch, '')
    
    def get_wuxing(self, stem_branch: str) -> Tuple[str, str]:
        """獲取五行 (簡化版)"""
        wuxing_stems = {
            '甲': '木', '乙': '木', '丙': '火', '丁': '火',
            '戊': '土', '己': '土', '庚': '金', '辛': '金',
            '壬': '水', '癸': '水'
        }
        
        wuxing_branches = {
            '子': '水', '丑': '土', '寅': '木', '卯': '木',
            '辰': '土', '巳': '火', '午': '火', '未': '土',
            '申': '金', '酉': '金', '戌': '土', '亥': '水'
        }
        
        stem = stem_branch[0]
        branch = stem_branch[1]
        
        return wuxing_stems.get(stem, ''), wuxing_branches.get(branch, '')


def main():
    calculator = BaziCalculator()
    
    print("八字排盤系統")
    print("=" * 30)
    
    try:
        # 讓用戶輸入出生日期時間
        year = int(input("請輸入出生年份 (例如: 1990): "))
        month = int(input("請輸入出生月份 (1-12): "))
        day = int(input("請輸入出生日期 (1-31): "))
        hour = int(input("請輸入出生時辰 (0-23): "))
        
        birth_datetime = datetime.datetime(year, month, day, hour)
        
        # 計算八字
        bazi = calculator.calculate_bazi(birth_datetime)
        
        # 顯示結果
        print("\n八字排盤結果:")
        print(f"出生日期: {birth_datetime.strftime('%Y年%m月%d日 %H時')}")
        
        print(f"\n年柱: {bazi['year']} ({calculator.get_zodiac_sign(bazi['year'][1])}年)")
        stem_wu, branch_wu = calculator.get_wuxing(bazi['year'])
        print(f"  五行: {stem_wu}/{branch_wu}")
        
        print(f"月柱: {bazi['month']}")
        stem_wu, branch_wu = calculator.get_wuxing(bazi['month'])
        print(f"  五行: {stem_wu}/{branch_wu}")
        
        print(f"日柱: {bazi['day']}")
        stem_wu, branch_wu = calculator.get_wuxing(bazi['day'])
        print(f"  五行: {stem_wu}/{branch_wu}")
        
        print(f"時柱: {bazi['hour']}")
        stem_wu, branch_wu = calculator.get_wuxing(bazi['hour'])
        print(f"  五行: {stem_wu}/{branch_wu}")
        
        print(f"\n完整八字: {bazi['year']} {bazi['month']} {bazi['day']} {bazi['hour']}")
        
    except ValueError:
        print("輸入格式錯誤，請重新運行程式。")
    except Exception as e:
        print(f"計算出錯: {str(e)}")


if __name__ == "__main__":
    main()