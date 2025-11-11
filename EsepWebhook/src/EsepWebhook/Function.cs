using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Amazon.Lambda.Core;
using Newtonsoft.Json;

// Assembly attribute to enable the Lambda function's JSON input to be converted into a .NET class.
[assembly: LambdaSerializer(typeof(Amazon.Lambda.Serialization.SystemTextJson.DefaultLambdaJsonSerializer))]

namespace EsepWebhook
{
    public class Function
    {
        private static readonly HttpClient httpClient = new HttpClient();

        public async Task<string> FunctionHandler(object input, ILambdaContext context)
        {
            string slackUrl = Environment.GetEnvironmentVariable("SLACK_URL");
            if (string.IsNullOrEmpty(slackUrl))
            {
                return "Missing SLACK_URL environment variable.";
            }

            dynamic payload = JsonConvert.DeserializeObject<dynamic>(input.ToString());
            string issueUrl = payload?.issue?.html_url;

            if (issueUrl == null)
                {
                    return "Non-issue event received. Ignored.";
                }

            string message = $"Issue Created: {issueUrl}";

            var slackPayload = new { text = message };
            var content = new StringContent(JsonConvert.SerializeObject(slackPayload), Encoding.UTF8, "application/json");

            var response = await httpClient.PostAsync(slackUrl, content);

            return $"Posted to Slack: {message}";
        }
    }
}
