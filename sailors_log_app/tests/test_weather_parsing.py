from sailors_log_app.services.weather import parse_weather

data = {
    'latitude': 54.86,
    'longitude': 10.5,
    'generationtime_ms': 23.725390434265137,
    'utc_offset_seconds': 0,
    'timezone': 'GMT',
    'timezone_abbreviation': 'GMT',
    'elevation': 0.0,
    'hourly_units': {
        'time': 'iso8601',
        'temperature_2m': '°C',
        'rain': 'mm',
        'weather_code': 'wmo code',
        'visibility': 'm',
        'wind_direction_10m': '°',
        'wind_speed_10m': 'kn',
        'wind_gusts_10m': 'kn',
        'cloud_cover': '%',
        'cloud_cover_low': '%',
        'cloud_cover_mid': '%',
        'cloud_cover_high': '%',
        'pressure_msl': 'hPa',
        'surface_pressure': 'hPa'
    },
    'hourly': {
        'time': [
            '2025-05-31T00:00',
            '2025-05-31T01:00',
            '2025-05-31T02:00',
            '2025-05-31T03:00',
            '2025-05-31T04:00',
            '2025-05-31T05:00',
            '2025-05-31T06:00',
            '2025-05-31T07:00',
            '2025-05-31T08:00',
            '2025-05-31T09:00',
            '2025-05-31T10:00',
            '2025-05-31T11:00',
            '2025-05-31T12:00',
            '2025-05-31T13:00',
            '2025-05-31T14:00',
            '2025-05-31T15:00',
            '2025-05-31T16:00',
            '2025-05-31T17:00',
            '2025-05-31T18:00',
            '2025-05-31T19:00',
            '2025-05-31T20:00',
            '2025-05-31T21:00',
            '2025-05-31T22:00',
            '2025-05-31T23:00',
            '2025-06-01T00:00',
            '2025-06-01T01:00',
            '2025-06-01T02:00',
            '2025-06-01T03:00',
            '2025-06-01T04:00',
            '2025-06-01T05:00',
            '2025-06-01T06:00',
            '2025-06-01T07:00',
            '2025-06-01T08:00',
            '2025-06-01T09:00',
            '2025-06-01T10:00',
            '2025-06-01T11:00',
            '2025-06-01T12:00',
            '2025-06-01T13:00',
            '2025-06-01T14:00',
            '2025-06-01T15:00',
            '2025-06-01T16:00',
            '2025-06-01T17:00',
            '2025-06-01T18:00',
            '2025-06-01T19:00',
            '2025-06-01T20:00',
            '2025-06-01T21:00',
            '2025-06-01T22:00',
            '2025-06-01T23:00'
        ],
        'temperature_2m': [
            13.4,
            13.3,
            13.1,
            12.9,
            13.2,
            13.6,
            13.9,
            14.4,
            15.0,
            16.0,
            17.4,
            17.9,
            18.6,
            19.0,
            19.2,
            18.6,
            17.7,
            17.5,
            16.0,
            15.0,
            14.3,
            14.3,
            14.2,
            14.1,
            14.5,
            14.4,
            14.6,
            14.9,
            14.9,
            14.9,
            15.6,
            16.2,
            15.9,
            17.0,
            18.0,
            17.8,
            19.0,
            17.4,
            17.2,
            18.1,
            18.4,
            17.1,
            16.2,
            14.8,
            13.6,
            13.0,
            12.2,
            12.2
        ],
        'rain': [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.2,
            0.0,
            0.0,
            0.0,
            0.0,
            0.3,
            1.1,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0
        ],
        'weather_code': [
            3,
            3,
            3,
            2,
            3,
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            1,
            1,
            1,
            1,
            1,
            1,
            0,
            0,
            0,
            2,
            3,
            3,
            2,
            3,
            3,
            3,
            3,
            3,
            61,
            80,
            80,
            1,
            2,
            3,
            80,
            80,
            3,
            3,
            3,
            3,
            0,
            1,
            3,
            2,
            2
        ],
        'visibility': [
            4120.0,
            4800.0,
            6040.0,
            5600.0,
            7400.0,
            7280.0,
            11580.0,
            14860.0,
            18420.0,
            27540.0,
            39400.0,
            43920.0,
            40180.0,
            40500.0,
            43320.0,
            35220.0,
            31620.0,
            31020.0,
            19340.0,
            13600.0,
            16120.0,
            10880.0,
            16100.0,
            15100.0,
            17140.0,
            18600.0,
            18440.0,
            14360.0,
            13240.0,
            9980.0,
            11680.0,
            6060.0,
            12760.0,
            26640.0,
            22240.0,
            21080.0,
            20700.0,
            13580.0,
            7480.0,
            12420.0,
            34980.0,
            38520.0,
            36360.0,
            30680.0,
            23920.0,
            27280.0,
            22340.0,
            23180.0
        ],
        'wind_direction_10m': [
            254,
            264,
            267,
            265,
            276,
            278,
            279,
            277,
            270,
            256,
            257,
            256,
            258,
            302,
            270,
            45,
            173,
            176,
            167,
            152,
            147,
            147,
            141,
            145,
            150,
            144,
            145,
            141,
            146,
            152,
            169,
            198,
            228,
            206,
            192,
            190,
            192,
            201,
            166,
            213,
            262,
            265,
            266,
            268,
            271,
            270,
            269,
            267
        ],
        'wind_speed_10m': [
            10.1,
            11.3,
            10.7,
            10.2,
            10.6,
            10.4,
            10.6,
            9.8,
            9.5,
            9.0,
            10.0,
            9.4,
            6.6,
            2.5,
            0.4,
            3.3,
            3.3,
            2.9,
            4.4,
            4.2,
            3.9,
            5.3,
            6.2,
            6.8,
            8.3,
            9.3,
            9.2,
            8.6,
            9.1,
            9.2,
            9.3,
            8.6,
            11.6,
            12.5,
            8.7,
            10.4,
            8.2,
            5.8,
            7.0,
            8.1,
            13.7,
            14.6,
            13.8,
            12.1,
            11.7,
            12.1,
            9.7,
            9.9
        ],
        'wind_gusts_10m': [
            14.6,
            17.5,
            18.3,
            16.7,
            17.1,
            16.3,
            16.7,
            16.9,
            15.7,
            16.7,
            18.7,
            17.3,
            14.8,
            11.1,
            4.7,
            7.2,
            7.0,
            5.4,
            7.0,
            7.0,
            7.0,
            7.6,
            9.7,
            10.5,
            14.6,
            15.2,
            15.4,
            14.2,
            14.4,
            15.2,
            14.6,
            14.6,
            21.8,
            18.7,
            19.0,
            20.0,
            16.7,
            13.6,
            12.6,
            11.3,
            20.2,
            23.5,
            24.7,
            20.8,
            18.3,
            18.5,
            17.5,
            16.9
        ],
        'cloud_cover': [
            86,
            100,
            90,
            82,
            91,
            55,
            83,
            79,
            75,
            52,
            82,
            85,
            100,
            85,
            67,
            3,
            14,
            30,
            38,
            5,
            2,
            0,
            45,
            96,
            78,
            48,
            100,
            100,
            100,
            100,
            100,
            100,
            100,
            57,
            2,
            83,
            100,
            99,
            100,
            100,
            100,
            100,
            100,
            0,
            9,
            100,
            78,
            66
        ],
        'cloud_cover_low': [
            86,
            100,
            90,
            82,
            91,
            55,
            83,
            79,
            75,
            52,
            78,
            85,
            59,
            84,
            67,
            3,
            14,
            30,
            38,
            5,
            2,
            0,
            45,
            41,
            64,
            47,
            50,
            29,
            21,
            30,
            4,
            27,
            0,
            43,
            2,
            22,
            50,
            50,
            67,
            100,
            54,
            0,
            37,
            0,
            0,
            0,
            76,
            66
        ],
        'cloud_cover_mid': [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            7,
            71,
            0,
            19,
            67,
            100,
            100,
            100,
            100,
            100,
            37,
            0,
            69,
            93,
            96,
            34,
            100,
            88,
            100,
            68,
            0,
            0,
            0,
            0,
            0
        ],
        'cloud_cover_high': [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            30,
            0,
            100,
            0,
            0,
            0,
            0,
            0,
            6,
            0,
            0,
            0,
            0,
            89,
            17,
            2,
            100,
            100,
            100,
            100,
            100,
            100,
            48,
            0,
            0,
            38,
            96,
            90,
            100,
            100,
            100,
            100,
            100,
            0,
            9,
            100,
            10,
            0
        ],
        'pressure_msl': [
            1016.7,
            1016.4,
            1016.8,
            1016.8,
            1016.6,
            1017.0,
            1017.1,
            1017.4,
            1018.3,
            1017.4,
            1018.3,
            1018.0,
            1017.7,
            1017.7,
            1017.6,
            1016.8,
            1016.9,
            1016.9,
            1016.5,
            1016.5,
            1016.6,
            1016.4,
            1016.1,
            1015.4,
            1014.9,
            1013.9,
            1013.5,
            1012.1,
            1011.5,
            1012.0,
            1011.4,
            1011.2,
            1010.7,
            1010.0,
            1010.1,
            1010.2,
            1009.8,
            1009.0,
            1008.7,
            1008.3,
            1008.7,
            1008.9,
            1010.0,
            1010.3,
            1010.6,
            1010.7,
            1010.7,
            1010.7
        ],
        'surface_pressure': [
            1016.7,
            1016.4,
            1016.8,
            1016.8,
            1016.6,
            1017.0,
            1017.1,
            1017.4,
            1018.3,
            1017.4,
            1018.3,
            1018.0,
            1017.7,
            1017.7,
            1017.6,
            1016.8,
            1016.9,
            1016.9,
            1016.5,
            1016.5,
            1016.6,
            1016.4,
            1016.1,
            1015.4,
            1014.9,
            1013.9,
            1013.5,
            1012.1,
            1011.5,
            1012.0,
            1011.4,
            1011.2,
            1010.7,
            1010.0,
            1010.1,
            1010.2,
            1009.8,
            1009.0,
            1008.7,
            1008.3,
            1008.7,
            1008.9,
            1010.0,
            1010.3,
            1010.6,
            1010.7,
            1010.7,
            1010.7
        ]
    }
}



def test_parse():
    for weather_snapshot in parse_weather(data):
        print(weather_snapshot)
