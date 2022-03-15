# ws_sb

캘린더 스프레드 전략 수립 및 백테스트 결과입니다.

★ 평균회귀 Rule Base 전략, ML/GRU 활용 예측 기반 전략 등으로 전략을 구성하였습니다.
★ 최종 결론 장표는 01_05_Strategy&Evaluation을 참고해주세요.

분석 순서

01_01_Preprocessing => 데이터 구조 변환 및 전처리

01_02_EDA => 기초분포, 상관분석, 정상성 검정, 공분산 검정 등

01_03_Feature_selection => IC, 다중공선성 기반 변수선택

01_04_01_Modeling_ML => RF 모델링

01_04_02_Restructure_GRU => GRU 학습 형태로 데이터 구조 변환

01_04_03_Modeling_GRU => GRU 모델링

01_05_Rule => 상방 임계점 초과시 매도, 하방 임계점 미만시 매수 전략

01_06_Strategy&Evaluation => 전략 구현 및 최종 성능 평가

evaluation_module => 전략 성능평가 함수를 구현한 모듈
