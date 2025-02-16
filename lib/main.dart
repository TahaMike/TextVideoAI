import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import 'package:textvideoai/provider.dart';
import 'dart:convert';

Future<String> generateVideo(String text) async {
  final url = Uri.parse('http://127.0.0.1:5000/generate'); 

  final response = await http.post(
    url,
    headers: {'Content-Type': 'application/json'},
    body: json.encode({'text': text}),
  );

  if (response.statusCode == 200) {
    final data = json.decode(response.body);
    return data['video_url'];
  } else {
    throw Exception('Failed to generate video');
  }
}

void main() {
  runApp(const ProviderScope(child: MyApp()));
}

class MyApp extends ConsumerWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final text = ref.watch(textProvider);
    return MaterialApp(
      title: 'Text to Video AI',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Text to Video AI'),
        ),
        body: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            children: [
              TextField(
                onChanged: (newText) {
                  ref.read(textProvider.notifier).state = newText;
                },
                decoration: const InputDecoration(
                  labelText: 'Enter Text',
                ),
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () async {
                  try {
                    String videoUrl = await generateVideo(text);
                    print('Generated Video URL: $videoUrl');
                  } catch (e) {
                    print('Error: $e');
                  }
                },
                child: const Text('Generate Video'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
