
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:io';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final cameras = await availableCameras();
  runApp(CropAdvisoryApp(cameras: cameras));
}

class CropAdvisoryApp extends StatelessWidget {
  final List<CameraDescription> cameras;

  const CropAdvisoryApp({Key? key, required this.cameras}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'জাতীয় ফসল স্বাস্থ্য পরামর্শ',
      theme: ThemeData(
        primarySwatch: Colors.green,
        fontFamily: 'Kalpurush',
        useMaterial3: true,
      ),
      home: HomeScreen(cameras: cameras),
      debugShowCheckedModeBanner: false,
    );
  }
}

class HomeScreen extends StatefulWidget {
  final List<CameraDescription> cameras;

  const HomeScreen({Key? key, required this.cameras}) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    final screens = [
      DiagnosisScreen(cameras: widget.cameras),
      const HistoryScreen(),
      const AdvisoryScreen(),
      const ProfileScreen(),
    ];

    return Scaffold(
      body: screens[_selectedIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _selectedIndex,
        onDestinationSelected: (index) => setState(() => _selectedIndex = index),
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.camera_alt),
            label: 'নির্ণয়',
          ),
          NavigationDestination(
            icon: Icon(Icons.history),
            label: 'ইতিহাস',
          ),
          NavigationDestination(
            icon: Icon(Icons.agriculture),
            label: 'পরামর্শ',
          ),
          NavigationDestination(
            icon: Icon(Icons.person),
            label: 'প্রোফাইল',
          ),
        ],
      ),
    );
  }
}

class DiagnosisScreen extends StatefulWidget {
  final List<CameraDescription> cameras;

  const DiagnosisScreen({Key? key, required this.cameras}) : super(key: key);

  @override
  State<DiagnosisScreen> createState() => _DiagnosisScreenState();
}

class _DiagnosisScreenState extends State<DiagnosisScreen> {
  File? _imageFile;
  String? _selectedCrop;
  bool _isLoading = false;
  Map<String, dynamic>? _result;

  final List<Map<String, String>> _crops = [
    {'id': 'rice', 'name': 'ধান', 'icon': '🌾'},
    {'id': 'eggplant', 'name': 'বেগুন', 'icon': '🍆'},
    {'id': 'tomato', 'name': 'টমেটো', 'icon': '🍅'},
    {'id': 'potato', 'name': 'আলু', 'icon': '🥔'},
    {'id': 'wheat', 'name': 'গম', 'icon': '🌾'},
    {'id': 'maize', 'name': 'ভুট্টা', 'icon': '🌽'},
    {'id': 'cabbage', 'name': 'বাঁধাকপি', 'icon': '🥬'},
    {'id': 'cauliflower', 'name': 'ফুলকপি', 'icon': '🥦'},
    {'id': 'okra', 'name': 'ঢেঁড়স', 'icon': '🌿'},
    {'id': 'cucumber', 'name': 'শসা', 'icon': '🥒'},
  ];

  Future<void> _takePicture() async {
    final image = await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => CameraScreen(camera: widget.cameras.first),
      ),
    );

    if (image != null) {
      setState(() => _imageFile = File(image.path));
    }
  }

  Future<void> _submitDiagnosis() async {
    if (_imageFile == null || _selectedCrop == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('ছবি এবং ফসল নির্বাচন করুন')),
      );
      return;
    }

    setState(() => _isLoading = true);

    try {
      final request = http.MultipartRequest(
        'POST',
        Uri.parse('https://api.cropadvisory.gov.bd/api/v1/diagnose'),
      );

      request.files.add(await http.MultipartFile.fromPath('image', _imageFile!.path));
      request.fields['crop'] = _selectedCrop!;
      request.fields['district'] = 'Dhaka'; // Get from GPS or user input
      request.fields['upazila'] = 'Dhanmondi';
      request.fields['phone_number'] = '01712345678';

      final response = await request.send();
      final responseData = await response.stream.bytesToString();

      setState(() {
        _result = json.decode(responseData);
        _isLoading = false;
      });

    } catch (e) {
      setState(() => _isLoading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('ত্রুটি: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('ফসল রোগ নির্ণয়'),
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Image capture section
            Card(
              child: InkWell(
                onTap: _takePicture,
                child: Container(
                  height: 200,
                  decoration: BoxDecoration(
                    color: Colors.grey[200],
                    borderRadius: BorderRadius.circular(12),
                    image: _imageFile != null
                        ? DecorationImage(
                            image: FileImage(_imageFile!),
                            fit: BoxFit.cover,
                          )
                        : null,
                  ),
                  child: _imageFile == null
                      ? Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: const [
                            Icon(Icons.camera_alt, size: 64, color: Colors.grey),
                            SizedBox(height: 8),
                            Text(
                              'ছবি তুলুন বা গ্যালারি থেকে নির্বাচন করুন',
                              style: TextStyle(color: Colors.grey),
                            ),
                          ],
                        )
                      : null,
                ),
              ),
            ),

            const SizedBox(height: 20),

            // Crop selection
            const Text(
              'ফসল নির্বাচন করুন:',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),

            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: _crops.map((crop) {
                final isSelected = _selectedCrop == crop['id'];
                return ChoiceChip(
                  label: Text('${crop['icon']} ${crop['name']}'),
                  selected: isSelected,
                  onSelected: (selected) {
                    setState(() => _selectedCrop = selected ? crop['id'] : null);
                  },
                  selectedColor: Colors.green[100],
                  checkmarkColor: Colors.green,
                );
              }).toList(),
            ),

            const SizedBox(height: 24),

            // Submit button
            ElevatedButton.icon(
              onPressed: _isLoading ? null : _submitDiagnosis,
              icon: _isLoading
                  ? const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : const Icon(Icons.search),
              label: Text(_isLoading ? 'বিশ্লেষণ হচ্ছে...' : 'রোগ নির্ণয় করুন'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
                textStyle: const TextStyle(fontSize: 18),
              ),
            ),

            // Results
            if (_result != null) ...[
              const SizedBox(height: 24),
              _buildResultCard(),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildResultCard() {
    final bangla = _result!['explanation_bangla'];
    final advisory = _result!['advisory'];

    return Card(
      color: Colors.green[50],
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              bangla['summary'],
              style: const TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Colors.green,
              ),
            ),
            const Divider(),
            Text(
              bangla['problem'],
              style: const TextStyle(fontSize: 16),
            ),
            const SizedBox(height: 12),
            const Text(
              '✅ করণীয়:',
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
            ),
            ...advisory['advice']['cultural'].take(3).map((item) => 
              Padding(
                padding: const EdgeInsets.only(left: 16, top: 4),
                child: Text('• $item'),
              ),
            ).toList(),
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.orange[50],
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: Colors.orange),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    '⚠️ সতর্কতা:',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  Text(_result!['disclaimer']),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class CameraScreen extends StatefulWidget {
  final CameraDescription camera;

  const CameraScreen({Key? key, required this.camera}) : super(key: key);

  @override
  State<CameraScreen> createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;

  @override
  void initState() {
    super.initState();
    _controller = CameraController(
      widget.camera,
      ResolutionPreset.high,
    );
    _initializeControllerFuture = _controller.initialize();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('ছবি তুলুন')),
      body: FutureBuilder<void>(
        future: _initializeControllerFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.done) {
            return CameraPreview(_controller);
          } else {
            return const Center(child: CircularProgressIndicator());
          }
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          try {
            await _initializeControllerFuture;
            final image = await _controller.takePicture();
            Navigator.pop(context, image);
          } catch (e) {
            print(e);
          }
        },
        child: const Icon(Icons.camera),
      ),
    );
  }
}

class HistoryScreen extends StatelessWidget {
  const HistoryScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('নির্ণয় ইতিহাস')),
      body: ListView.builder(
        itemCount: 10,
        itemBuilder: (context, index) {
          return ListTile(
            leading: const Icon(Icons.history, color: Colors.green),
            title: Text('ধান - ${_getRandomDate(index)}'),
            subtitle: const Text('সম্ভাব্য: ছত্রাকজনিত রোগ'),
            trailing: const Icon(Icons.chevron_right),
          );
        },
      ),
    );
  }

  String _getRandomDate(int index) {
    final dates = ['২ দিন আগে', '৫ দিন আগে', '১ সপ্তাহ আগে', '২ সপ্তাহ আগে'];
    return dates[index % dates.length];
  }
}

class AdvisoryScreen extends StatelessWidget {
  const AdvisoryScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('কৃষি পরামর্শ')),
      body: ListView(
        children: [
          _buildAdvisoryCard(
            'ধানের রোগ ব্যবস্থাপনা',
            'BRRI নির্দেশনা অনুযায়ী',
            Icons.grain,
          ),
          _buildAdvisoryCard(
            'বেগুনের পোকা দমন',
            'IPM পদ্ধতি',
            Icons.eco,
          ),
          _buildAdvisoryCard(
            'সুষম সার ব্যবহার',
            'SRDI সার সুপারিশ',
            Icons.agriculture,
          ),
          _buildAdvisoryCard(
            'জৈবিক দমন পদ্ধতি',
            'বালাই ফাঁদ ও প্রাকৃতিক শত্রু',
            Icons.bug_report,
          ),
        ],
      ),
    );
  }

  Widget _buildAdvisoryCard(String title, String subtitle, IconData icon) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: ListTile(
        leading: Icon(icon, color: Colors.green, size: 40),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
        subtitle: Text(subtitle),
        trailing: const Icon(Icons.arrow_forward_ios),
        onTap: () {},
      ),
    );
  }
}

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('প্রোফাইল')),
      body: Column(
        children: [
          const SizedBox(height: 20),
          const CircleAvatar(
            radius: 50,
            backgroundColor: Colors.green,
            child: Icon(Icons.person, size: 50, color: Colors.white),
          ),
          const SizedBox(height: 16),
          const Text(
            'কৃষক',
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          ),
          const Text(
            'ঢাকা জেলা, ধানমন্ডি উপজেলা',
            style: TextStyle(color: Colors.grey),
          ),
          const SizedBox(height: 32),
          _buildProfileMenuItem(Icons.phone, 'হেল্পলাইন: 16263'),
          _buildProfileMenuItem(Icons.location_on, 'আমার ক্ষেতের অবস্থান'),
          _buildProfileMenuItem(Icons.settings, 'সেটিংস'),
          _buildProfileMenuItem(Icons.help, 'সাহায্য ও জিজ্ঞাসা'),
        ],
      ),
    );
  }

  Widget _buildProfileMenuItem(IconData icon, String title) {
    return ListTile(
      leading: Icon(icon, color: Colors.green),
      title: Text(title),
      trailing: const Icon(Icons.chevron_right),
      onTap: () {},
    );
  }
}
