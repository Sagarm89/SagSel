using System.Text.Json.Serialization;

namespace OpenQA.Selenium.DevTools.V85;

[JsonSerializable(typeof(ICommand))]
internal sealed partial class V85RequestSerializationContext : JsonSerializerContext;

[JsonSerializable(typeof(ICommand))]
internal sealed partial class V85ResponseSerializationContext : JsonSerializerContext;
