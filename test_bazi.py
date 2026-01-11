from bazi_calculator import BaziCalculator
import datetime

# 測試八字計算器
calculator = BaziCalculator()

# 測試幾個日期
test_dates = [
    datetime.datetime(1990, 5, 15, 14),  # 1990年5月15日下午2點
    datetime.datetime(1984, 2, 16, 8),   # 1984年2月16日上午8點 (甲子年)
    datetime.datetime(2000, 1, 1, 0),    # 2000年1月1日凌晨0點
    datetime.datetime(2023, 12, 25, 19)  # 2023年12月25日晚上7點
]

print("八字排盤測試")
print("=" * 50)

for birth_datetime in test_dates:
    print(f"\n測試日期: {birth_datetime.strftime('%Y年%m月%d日 %H時')}")
    
    # 計算八字
    bazi = calculator.calculate_bazi(birth_datetime)
    
    # 顯示結果
    print(f"年柱: {bazi['year']} ({calculator.get_zodiac_sign(bazi['year'][1])}年)")
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
    
    print(f"完整八字: {bazi['year']} {bazi['month']} {bazi['day']} {bazi['hour']}")
    print("-" * 30)