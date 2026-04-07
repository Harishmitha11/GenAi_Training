import { useMemo, useState } from 'react';
import {
  Box,
  Button,
  Code,
  Container,
  Divider,
  Flex,
  Heading,
  Input,
  Select,
  SimpleGrid,
  Stack,
  Text,
  Textarea,
  useToast,
  VStack,
} from '@chakra-ui/react';

const sampleProtocol = `Protocol title: Early-phase oncology study\n\nInclusion criteria:\n- Age 18-75\n- Confirmed diagnosis of stage II/III solid tumor\n- ECOG performance status 0-1\n- Adequate hepatic and renal function\n\nExclusion criteria:\n- Active uncontrolled infection\n- Prior immunotherapy within 4 weeks\n- Significant cardiovascular disease\n`;

const samplePatient = {
  patientId: 'P-1001',
  age: 62,
  diagnoses: ['Stage II breast cancer'],
  medications: ['aspirin'],
  labs: {
    creatinine: 0.9,
    bilirubin: 0.8,
  },
  performanceStatus: 1,
};

function evaluateMatch(protocolText: string, patientData: any) {
  const reasons: string[] = [];
  const matched = [];
  const failed = [];

  if (patientData.age >= 18 && patientData.age <= 75) {
    matched.push('Age within trial range');
  } else {
    failed.push('Age outside protocol eligibility');
  }

  if (patientData.performanceStatus <= 1) {
    matched.push('ECOG performance meets criteria');
  } else {
    failed.push('Performance status too high');
  }

  if (patientData.diagnoses.some((d: string) => /stage II|stage III/i.test(d))) {
    matched.push('Diagnosis matches inclusion criteria');
  } else {
    failed.push('Diagnosis not in stated tumor stage range');
  }

  if (patientData.labs.creatinine <= 1.5 && patientData.labs.bilirubin <= 1.5) {
    matched.push('Lab values are within acceptable limits');
  } else {
    failed.push('Lab values may violate renal/hepatic cutoffs');
  }

  if (patientData.medications.some((m: string) => /immunotherapy/i.test(m))) {
    failed.push('Recent immunotherapy may exclude patient');
  }

  const score = Math.max(0, 100 - failed.length * 20);
  return { score, matched, failed, reasons };
}

function App() {
  const [protocolText, setProtocolText] = useState(sampleProtocol);
  const [patientJson, setPatientJson] = useState(JSON.stringify(samplePatient, null, 2));
  const [result, setResult] = useState<{ score: number; matched: string[]; failed: string[] } | null>(null);
  const [patientSource, setPatientSource] = useState('manual');
  const toast = useToast();

  const patient = useMemo(() => {
    try {
      return JSON.parse(patientJson);
    } catch {
      return null;
    }
  }, [patientJson]);

  const onRunMatch = () => {
    if (!patient) {
      toast({
        title: 'Invalid patient data',
        description: 'Please provide valid JSON for the patient profile.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      return;
    }

    const evaluation = evaluateMatch(protocolText, patient);
    setResult(evaluation);
  };

  return (
    <Box minH="100vh" bg="gray.50" py={8}>
      <Container maxW="7xl">
        <Stack spacing={8}>
          <Box p={6} bg="white" borderRadius="xl" boxShadow="md">
            <Heading size="lg" mb={2}>
              Clinical Trial Eligibility Playground
            </Heading>
            <Text color="gray.600">
              Simulate an eligibility match using a protocol and patient record. This UI is built with Chakra UI for a clean and responsive experience.
            </Text>
          </Box>

          <SimpleGrid columns={{ base: 1, lg: 2 }} spacing={6}>
            <Box p={6} bg="white" borderRadius="xl" boxShadow="sm">
              <Heading size="md" mb={4}>
                Trial Protocol
              </Heading>
              <Textarea
                minH="300px"
                value={protocolText}
                onChange={(event) => setProtocolText(event.target.value)}
                placeholder="Paste clinical trial protocol text here"
              />
            </Box>

            <Box p={6} bg="white" borderRadius="xl" boxShadow="sm">
              <Heading size="md" mb={4}>
                Patient Profile
              </Heading>
              <Flex gap={3} mb={4} alignItems="center">
                <Text fontWeight="semibold">Source:</Text>
                <Select value={patientSource} onChange={(e) => setPatientSource(e.target.value)} width="180px">
                  <option value="manual">Manual JSON</option>
                  <option value="ehr">EHR Extract</option>
                </Select>
              </Flex>
              <Textarea
                minH="300px"
                value={patientJson}
                onChange={(event) => setPatientJson(event.target.value)}
                placeholder="Enter patient data as JSON"
              />
            </Box>
          </SimpleGrid>

          <Flex justifyContent="space-between" alignItems="center">
            <Button colorScheme="blue" size="lg" onClick={onRunMatch}>
              Evaluate Eligibility
            </Button>
            <Text color="gray.600">Results are computed locally in this prototype.</Text>
          </Flex>

          <Box p={6} bg="white" borderRadius="xl" boxShadow="sm">
            <Heading size="md" mb={4}>
              Match Summary
            </Heading>
            {result ? (
              <Stack spacing={4}>
                <Flex justifyContent="space-between" alignItems="center">
                  <Text fontSize="lg" fontWeight="bold">
                    Score: {result.score}%
                  </Text>
                  <Text color={result.score >= 60 ? 'green.600' : 'orange.600'}>
                    {result.score >= 60 ? 'Candidate likely eligible' : 'Candidate may not be eligible'}
                  </Text>
                </Flex>
                <Box>
                  <Text fontWeight="semibold" mb={2}>
                    Criteria matched
                  </Text>
                  <Stack spacing={2}>
                    {result.matched.map((item) => (
                      <Box key={item} p={3} bg="green.50" borderRadius="md">
                        {item}
                      </Box>
                    ))}
                  </Stack>
                </Box>
                <Box>
                  <Text fontWeight="semibold" mb={2}>
                    Criteria failed
                  </Text>
                  <Stack spacing={2}>
                    {result.failed.map((item) => (
                      <Box key={item} p={3} bg="orange.50" borderRadius="md">
                        {item}
                      </Box>
                    ))}
                  </Stack>
                </Box>
              </Stack>
            ) : (
              <Text color="gray.600">Run an evaluation to see eligibility output and evidence.</Text>
            )}
          </Box>

          <Box p={6} bg="white" borderRadius="xl" boxShadow="sm">
            <Heading size="md" mb={4}>
              Implementation notes
            </Heading>
            <Text mb={3}>
              This prototype demonstrates a UI for protocol ingestion, patient capture, and eligibility summarization. A production implementation would connect this frontend to a LangChain backend with document retrieval, vector search, and compliance-aware audit logging.
            </Text>
            <Code>npm install</Code>
            <Code>npm run dev</Code>
          </Box>
        </Stack>
      </Container>
    </Box>
  );
}

export default App;
